from functools import reduce
from typing import Callable, List, Tuple
from ups_lib.rate_web_service_schema import (
    RateRequest as UPSRateRequest,
    RatedShipmentType,
    ShipmentRatingOptionsType,
    ShipToType,
    ShipmentType,
    ShipperType,
    ShipAddressType,
    ShipToAddressType,
    PackageType,
    PackageWeightType,
    UOMCodeDescriptionType,
    DimensionsType,
    RequestType,
    TransactionReferenceType,
    TimeInTransitRequestType,
    EstimatedArrivalType,
)
from purplship.core.utils import (
    apply_namespaceprefix,
    create_envelope,
    Serializable,
    Envelope,
    Element,
    SF,
    NF,
    XP,
)
from purplship.core.units import Packages, Services
from purplship.core.models import RateDetails, ChargeDetails, Message, RateRequest
from purplship.providers.ups.units import (
    RatingServiceCode,
    RatingPackagingType,
    WeightUnit as UPSWeightUnit,
    ShippingServiceCode,
    PackagePresets,
)
from purplship.providers.ups.error import parse_error_response
from purplship.providers.ups.utils import Settings


def parse_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    rate_reply = XP.find("RatedShipment", response)
    rates: List[RateDetails] = reduce(_extract_package_rate(settings), rate_reply, [])
    return rates, parse_error_response(response, settings)


def _extract_package_rate(
    settings: Settings,
) -> Callable[[List[RateDetails], Element], List[RateDetails]]:
    def extract(rates: List[RateDetails], detail_node: Element) -> List[RateDetails]:
        rate = XP.build(RatedShipmentType, detail_node)

        if rate.NegotiatedRateCharges is not None:
            total_charges = (
                rate.NegotiatedRateCharges.TotalChargesWithTaxes
                or rate.NegotiatedRateCharges.TotalCharge
            )
            taxes = rate.NegotiatedRateCharges.TaxCharges
            itemized_charges = rate.NegotiatedRateCharges.ItemizedCharges + taxes
        else:
            total_charges = rate.TotalChargesWithTaxes or rate.TotalCharges
            taxes = rate.TaxCharges
            itemized_charges = rate.ItemizedCharges + taxes

        extra_charges = itemized_charges + [rate.ServiceOptionsCharges]
        estimated_arrival = (
            XP.find("EstimatedArrival", detail_node, EstimatedArrivalType, first=True)
            or EstimatedArrivalType()
        )
        transit_days = (
            rate.GuaranteedDelivery.BusinessDaysInTransit
            if rate.GuaranteedDelivery is not None
            else estimated_arrival.BusinessDaysInTransit
        )
        currency = XP.find("CurrencyCode", detail_node, first=True).text
        service = ShippingServiceCode.map(rate.Service.Code)

        return rates + [
            RateDetails(
                carrier_name=settings.carrier_name,
                carrier_id=settings.carrier_id,
                currency=currency,
                service=service.name_or_key,
                base_charge=NF.decimal(rate.TransportationCharges.MonetaryValue),
                total_charge=NF.decimal(total_charges.MonetaryValue),
                duties_and_taxes=reduce(
                    lambda total, charge: total + NF.decimal(charge.MonetaryValue),
                    taxes or [],
                    0.0,
                ),
                extra_charges=reduce(
                    lambda total, charge: (
                        total
                        + [
                            ChargeDetails(
                                name=charge.Code,
                                amount=NF.decimal(charge.MonetaryValue),
                                currency=charge.CurrencyCode,
                            )
                        ]
                    ),
                    [charge for charge in extra_charges if charge is not None],
                    [],
                ),
                transit_days=NF.integer(transit_days),
                meta=dict(service_name=service.name_or_key)
            )
        ]

    return extract


def rate_request(
    payload: RateRequest, settings: Settings
) -> Serializable[UPSRateRequest]:
    packages = Packages(payload.parcels, PackagePresets)
    is_document = all([parcel.is_document for parcel in payload.parcels])
    service = Services(payload.services, RatingServiceCode).first

    if (
        (service is not None)
        and (("freight" in service.value) or ("ground" in service.value))
    ):
        packages.validate(required=["weight"])

    mps_packaging = RatingPackagingType.ups_unknown.value if len(packages) > 1 else None

    request = UPSRateRequest(
        Request=RequestType(
            RequestOption=["Shop", "Rate"],
            SubVersion=None,
            TransactionReference=TransactionReferenceType(
                CustomerContext=payload.reference,
                TransactionIdentifier=getattr(payload, 'id', None)
            ),
        ),
        PickupType=None,
        CustomerClassification=None,
        Shipment=ShipmentType(
            OriginRecordTransactionTimestamp=None,
            Shipper=ShipperType(
                Name=payload.shipper.company_name,
                ShipperNumber=settings.account_number,
                Address=ShipAddressType(
                    AddressLine=SF.concat_str(
                        payload.recipient.address_line1,
                        payload.recipient.address_line2,
                    ),
                    City=payload.shipper.city,
                    StateProvinceCode=payload.shipper.state_code,
                    PostalCode=payload.shipper.postal_code,
                    CountryCode=payload.shipper.country_code,
                ),
            ),
            ShipTo=ShipToType(
                Name=payload.recipient.company_name,
                Address=ShipToAddressType(
                    AddressLine=SF.concat_str(
                        payload.recipient.address_line1,
                        payload.recipient.address_line2,
                    ),
                    City=payload.recipient.city,
                    StateProvinceCode=payload.recipient.state_code,
                    PostalCode=payload.recipient.postal_code,
                    CountryCode=payload.recipient.country_code,
                    ResidentialAddressIndicator=None,
                ),
            ),
            ShipFrom=None,
            AlternateDeliveryAddress=None,
            ShipmentIndicationType=None,
            PaymentDetails=None,
            FRSPaymentInformation=None,
            FreightShipmentInformation=None,
            GoodsNotInFreeCirculationIndicator=None,
            Service=(
                UOMCodeDescriptionType(Code=service.value, Description=None)
                if service is not None else None
            ),
            NumOfPieces=None,  # Only required for Freight
            ShipmentTotalWeight=None,  # Only required for "timeintransit" requests
            DocumentsOnlyIndicator="" if is_document else None,
            Package=[
                PackageType(
                    PackagingType=UOMCodeDescriptionType(
                        Code=(
                            mps_packaging or RatingPackagingType[
                                package.packaging_type or "small_box"
                            ].value
                        ),
                        Description=None,
                    ),
                    Dimensions=DimensionsType(
                        UnitOfMeasurement=UOMCodeDescriptionType(
                            Code=package.dimension_unit.value, Description=None
                        ),
                        Length=package.length.value,
                        Width=package.width.value,
                        Height=package.height.value,
                    )
                    if any(
                        [
                            package.length.value,
                            package.height.value,
                            package.width.value,
                        ]
                    )
                    else None,
                    DimWeight=None,
                    PackageWeight=PackageWeightType(
                        UnitOfMeasurement=UOMCodeDescriptionType(
                            Code=UPSWeightUnit[package.weight_unit.name].value,
                            Description=None,
                        ),
                        Weight=package.weight.value,
                    )
                    if package.weight.value
                    else None,
                    Commodity=None,
                    PackageServiceOptions=None,
                    AdditionalHandlingIndicator=None,
                )
                for package in packages
            ],
            ShipmentServiceOptions=None,
            ShipmentRatingOptions=ShipmentRatingOptionsType(
                NegotiatedRatesIndicator=""
            ),
            InvoiceLineTotal=None,
            RatingMethodRequestedIndicator=None,
            TaxInformationIndicator=None,
            PromotionalDiscountInformation=None,
            DeliveryTimeInformation=TimeInTransitRequestType(
                PackageBillType="02" if is_document else "03"
            ),
        ),
    )
    return Serializable(
        create_envelope(header_content=settings.Security, body_content=request),
        _request_serializer,
    )


def _request_serializer(envelope: Envelope) -> str:
    namespace_ = """
        xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"
        xmlns:rate="http://www.ups.com/XMLSchema/XOLTWS/Rate/v1.1"
    """.replace(
        " ", ""
    ).replace(
        "\n", " "
    )
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    envelope.Header.ns_prefix_ = envelope.ns_prefix_
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "rate")
    apply_namespaceprefix(envelope.Header.anytypeobjs_[0], "upss")
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0].Request, "common")

    return XP.export(envelope, namespacedef_=namespace_)
