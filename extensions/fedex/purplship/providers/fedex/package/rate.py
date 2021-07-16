from datetime import datetime
from typing import Tuple, List, Optional, cast
from fedex_lib.rate_service_v28 import (
    RateRequest as FedexRateRequest,
    RateReplyDetail,
    TransactionDetail,
    VersionId,
    RequestedShipment,
    TaxpayerIdentification,
    Party,
    Contact,
    Address,
    Money,
    Weight as FedexWeight,
    ShipmentRateDetail,
    Surcharge,
    RequestedPackageLineItem,
    Dimensions,
    CustomerReference,
    CustomerReferenceType,
)
from purplship.core.utils import create_envelope, apply_namespaceprefix, Element, Serializable, NF, XP, DF
from purplship.core.units import Packages, Options, Services, CompleteAddress
from purplship.core.models import RateDetails, RateRequest, Message, ChargeDetails
from purplship.providers.fedex.units import PackagingType, ServiceType, PackagePresets, MeasurementOptions
from purplship.providers.fedex.error import parse_error_response
from purplship.providers.fedex.utils import Settings


def parse_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    replys = XP.find("RateReplyDetails", response)
    rates: List[RateDetails] = [
        _extract_rate(detail_node, settings) for detail_node in replys
    ]
    return rates, parse_error_response(response, settings)


def _extract_rate(detail_node: Element, settings: Settings) -> Optional[RateDetails]:
    rate: RateReplyDetail = XP.build(RateReplyDetail, detail_node)
    service = ServiceType.map(rate.ServiceType)
    rate_type = rate.ActualRateType
    shipment_rate, shipment_discount = cast(
        Tuple[ShipmentRateDetail, Money],
        next(
            (
                (r.ShipmentRateDetail, r.EffectiveNetDiscount)
                for r in rate.RatedShipmentDetails
                if cast(ShipmentRateDetail, r.ShipmentRateDetail).RateType == rate_type
            ),
            (None, None),
        ),
    )
    discount = (
        NF.decimal(shipment_discount.Amount) if shipment_discount is not None else None
    )
    currency = cast(Money, shipment_rate.TotalBaseCharge).Currency
    duties_and_taxes = (
        shipment_rate.TotalTaxes.Amount + shipment_rate.TotalDutiesAndTaxes.Amount
    )
    surcharges = [
        ChargeDetails(
            name=cast(Surcharge, s).Description,
            amount=NF.decimal(cast(Surcharge, s).Amount.Amount),
            currency=currency,
        )
        for s in shipment_rate.Surcharges + shipment_rate.Taxes
    ]
    estimated_delivery = DF.date(rate.DeliveryTimestamp)
    transit = (
        ((estimated_delivery.date() - datetime.today().date()).days or None)
        if estimated_delivery is not None else None
    )

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service=service.name_or_key,
        currency=currency,
        base_charge=NF.decimal(shipment_rate.TotalBaseCharge.Amount),
        total_charge=NF.decimal(shipment_rate.TotalNetChargeWithDutiesAndTaxes.Amount),
        duties_and_taxes=NF.decimal(duties_and_taxes),
        discount=discount,
        transit_days=transit,
        extra_charges=surcharges,
        meta=dict(service_name=service.name_or_key)
    )


def rate_request(
    payload: RateRequest, settings: Settings
) -> Serializable[FedexRateRequest]:
    shipper = CompleteAddress.map(payload.shipper)
    recipient = CompleteAddress.map(payload.recipient)
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])
    service = Services(payload.services, ServiceType).first
    options = Options(payload.options)

    request_types = ["LIST"] + ([] if "currency" not in options else ["PREFERRED"])

    request = FedexRateRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(CustomerTransactionId="FTC"),
        Version=VersionId(ServiceId="crs", Major=28, Intermediate=0, Minor=0),
        ReturnTransitAndCommit=True,
        CarrierCodes=None,
        VariableOptions=None,
        ConsolidationKey=None,
        RequestedShipment=RequestedShipment(
            ShipTimestamp=DF.date(options.shipment_date or datetime.now()),
            DropoffType="REGULAR_PICKUP",
            ServiceType=(service.value if service is not None else None),
            PackagingType=PackagingType[packages.package_type or 'your_packaging'].value,
            VariationOptions=None,
            TotalWeight=FedexWeight(
                Units=packages.weight.unit,
                Value=packages.weight.LB,
            ),
            TotalInsuredValue=None,
            PreferredCurrency=options.currency,
            ShipmentAuthorizationDetail=None,
            Shipper=Party(
                AccountNumber=settings.account_number,
                Tins=(
                    [TaxpayerIdentification(Number=tax) for tax in shipper.taxes]
                    if shipper.has_tax_info else None
                ),
                Contact=(
                    Contact(
                        ContactId=None,
                        PersonName=shipper.person_name,
                        Title=None,
                        CompanyName=shipper.company_name,
                        PhoneNumber=shipper.phone_number,
                        PhoneExtension=None,
                        TollFreePhoneNumber=None,
                        PagerNumber=None,
                        FaxNumber=None,
                        EMailAddress=shipper.email,
                    )
                    if shipper.has_contact_info else None
                ),
                Address=Address(
                    StreetLines=shipper.address_lines,
                    City=shipper.city,
                    StateOrProvinceCode=shipper.state_code,
                    PostalCode=shipper.postal_code,
                    UrbanizationCode=None,
                    CountryCode=shipper.country_code,
                    CountryName=shipper.country_name,
                    Residential=shipper.residential,
                    GeographicCoordinates=None,
                ),
            ),
            Recipient=Party(
                AccountNumber=None,
                Tins=(
                    [TaxpayerIdentification(Number=tax) for tax in recipient.taxes]
                    if recipient.has_tax_info else None
                ),
                Contact=(
                    Contact(
                        ContactId=None,
                        PersonName=recipient.person_name,
                        Title=None,
                        CompanyName=recipient.company_name,
                        PhoneNumber=recipient.phone_number,
                        PhoneExtension=None,
                        TollFreePhoneNumber=None,
                        PagerNumber=None,
                        FaxNumber=None,
                        EMailAddress=recipient.email,
                    )
                    if recipient.has_contact_info else None
                ),
                Address=Address(
                    StreetLines=recipient.address_lines,
                    City=recipient.city,
                    StateOrProvinceCode=recipient.state_code,
                    PostalCode=recipient.postal_code,
                    UrbanizationCode=None,
                    CountryCode=recipient.country_code,
                    CountryName=recipient.country_name,
                    Residential=recipient.residential,
                    GeographicCoordinates=None,
                ),
            ),
            RecipientLocationNumber=None,
            Origin=None,
            SoldTo=None,
            ShippingChargesPayment=None,
            SpecialServicesRequested=None,
            ExpressFreightDetail=None,
            FreightShipmentDetail=None,
            DeliveryInstructions=None,
            VariableHandlingChargeDetail=None,
            CustomsClearanceDetail=None,
            PickupDetail=None,
            SmartPostDetail=None,
            BlockInsightVisibility=None,
            LabelSpecification=None,
            ShippingDocumentSpecification=None,
            RateRequestTypes=request_types,
            EdtRequestType=None,
            PackageCount=len(packages),
            ShipmentOnlyFields=None,
            ConfigurationData=None,
            RequestedPackageLineItems=[
                RequestedPackageLineItem(
                    SequenceNumber=index,
                    GroupNumber=None,
                    GroupPackageCount=1,
                    VariableHandlingChargeDetail=None,
                    InsuredValue=None,
                    Weight=(
                        FedexWeight(
                            Units=package.weight.unit,
                            Value=package.weight.value,
                        )
                        if package.weight.value else None
                    ),
                    Dimensions=(
                        Dimensions(
                            Length=package.length.map(MeasurementOptions).value,
                            Width=package.width.map(MeasurementOptions).value,
                            Height=package.height.map(MeasurementOptions).value,
                            Units=package.dimension_unit.value,
                        )
                        if package.has_dimensions else None
                    ),
                    PhysicalPackaging=None,
                    ItemDescription=package.parcel.description,
                    ItemDescriptionForClearance=None,
                    CustomerReferences=(
                        [
                            CustomerReference(
                                CustomerReferenceType=CustomerReferenceType.CUSTOMER_REFERENCE,
                                Value=payload.reference
                            )
                        ]
                        if any(payload.reference or "") else None
                    ),
                    SpecialServicesRequested=None,
                    ContentRecords=None,
                )
                for index, package in enumerate(packages, 1)
            ],
        ),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: FedexRateRequest) -> str:
    namespacedef_ = 'xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:v28="http://fedex.com/ws/rate/v28"'

    envelope = create_envelope(body_content=request)
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "v28")

    return XP.export(envelope, namespacedef_=namespacedef_)
