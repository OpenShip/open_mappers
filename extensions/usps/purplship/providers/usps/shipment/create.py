from typing import Tuple, List
from usps_lib.evs_response import eVSResponse
from usps_lib.evs_request import (
    eVSRequest,
    ImageParametersType,
    LabelSequenceType,
    ShippingContentsType,
    ItemDetailType,
    ExtraServicesType,
)
from purplship.core.errors import OriginNotServicedError, DestinationNotServicedError
from purplship.core.units import Packages, Options, WeightUnit, Weight, Country
from purplship.core.utils import Serializable, Element, Location, XP
from purplship.core.models import (
    ShipmentRequest,
    ShipmentDetails,
    ChargeDetails,
    Message,
    Address,
    Customs,
)

from purplship.providers.usps.units import (
    LabelFormat, ServiceType, PackagingType, ShipmentOption, ContentType
)
from purplship.providers.usps.error import parse_error_response
from purplship.providers.usps.utils import Settings


def parse_shipment_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    errors = parse_error_response(response, settings)
    details = _extract_details(response, settings)

    return details, errors


def _extract_details(response: Element, settings: Settings) -> ShipmentDetails:
    shipment = XP.build(eVSResponse, response)

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        label=shipment.LabelImage,
        tracking_number=shipment.BarcodeNumber,
        shipment_identifier=shipment.BarcodeNumber,
    )


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[eVSRequest]:
    if payload.shipper.country_code is not None and payload.shipper.country_code != Country.US.name:
        raise OriginNotServicedError(payload.shipper.country_code)

    if payload.recipient.country_code is not None and payload.recipient.country_code != Country.US.name:
        raise DestinationNotServicedError(payload.recipient.country_code)

    service = ServiceType.map(payload.service).value_or_key
    package = Packages(payload.parcels).single
    options = Options(payload.options, ShipmentOption)

    customs = payload.customs or Customs(commodities=[])
    extra_services = [getattr(option, 'value', option) for key, option in options if 'usps_option' not in key]
    label_format = LabelFormat[payload.label_type or 'usps_6_x_4_label'].value
    insurance = next((option.value for key, option in options if 'usps_insurance' in key), options.insurance)
    # Gets the first provided non delivery option or default to "RETURN"
    non_delivery = next((option.value for name, option in options if 'non_delivery' in name), "RETURN")
    redirect_address = Address(**(options.usps_option_redirect_non_delivery or {}))

    request = eVSRequest(
        USERID=settings.username,
        Option=None,
        Revision="1",
        ImageParameters=ImageParametersType(
            ImageParameter=label_format,
            LabelSequence=LabelSequenceType(PackageNumber=1, TotalPackages=1)
        ),
        FromName=payload.shipper.person_name,
        FromFirm=payload.shipper.company_name or "N/A",
        FromAddress1=payload.shipper.address_line2,
        FromAddress2=payload.shipper.address_line1,
        FromCity=payload.shipper.city,
        FromState=payload.shipper.state_code,
        FromZip5=Location(payload.shipper.postal_code).as_zip5 or "",
        FromZip4=Location(payload.shipper.postal_code).as_zip4 or "",
        FromPhone=payload.shipper.phone_number,
        POZipCode=None,
        AllowNonCleansedOriginAddr=False,
        ToName=payload.recipient.person_name,
        ToFirm=payload.recipient.company_name or "N/A",
        ToAddress1=payload.recipient.address_line2,
        ToAddress2=payload.recipient.address_line1,
        ToCity=payload.recipient.city,
        ToState=payload.recipient.state_code,
        ToZip5=Location(payload.recipient.postal_code).as_zip5 or "",
        ToZip4=Location(payload.recipient.postal_code).as_zip4 or "",
        ToPhone=payload.recipient.phone_number,
        POBox=None,
        ToContactPreference=None,
        ToContactMessaging=payload.recipient.email,
        ToContactEmail=payload.recipient.email,
        AllowNonCleansedDestAddr=False,
        WeightInOunces=package.weight.OZ,
        ServiceType=service,
        Container=PackagingType[package.packaging_type or 'variable'].value,
        Width=package.width.IN,
        Length=package.length.IN,
        Height=package.height.IN,
        Girth=(package.girth.value if package.packaging_type == "tube" else None),
        Machinable=options.usps_option_machinable_item,
        ProcessingCategory=None,
        PriceOptions=None,
        InsuredAmount=insurance,
        AddressServiceRequested=None,
        ExpressMailOptions=None,
        ShipDate=options.shipment_date,
        CustomerRefNo=None,
        ExtraServices=(
            ExtraServicesType(ExtraService=[s for s in extra_services])
            if any(extra_services) else None
        ),
        CRID=settings.customer_registration_id,
        MID=settings.mailer_id,
        LogisticsManagerMID=settings.logistics_manager_mailer_id,
        VendorCode=None,
        VendorProductVersionNumber=None,
        SenderName=(payload.shipper.person_name or payload.shipper.company_name),
        SenderEMail=payload.shipper.email,
        RecipientName=(payload.recipient.person_name or payload.recipient.company_name),
        RecipientEMail=payload.recipient.email,
        ReceiptOption="SEPARATE PAGE",
        ImageType="PDF",
        HoldForManifest=None,
        NineDigitRoutingZip=None,
        ShipInfo=options.usps_option_ship_info,
        CarrierRelease=None,
        DropOffTime=None,
        ReturnCommitments=None,
        PrintCustomerRefNo=None,
        Content=None,
        ShippingContents=(
            ShippingContentsType(
                ItemDetail=[
                    ItemDetailType(
                        Description=item.description,
                        Quantity=item.quantity,
                        Value=item.value_amount,
                        NetPounds=Weight(item.weight, WeightUnit[item.weight_unit or 'LB']).LB,
                        NetOunces=Weight(item.weight, WeightUnit[item.weight_unit or 'LB']).OZ,
                        HSTariffNumber=item.sku,
                        CountryOfOrigin=Location(item.origin_country).as_country_name
                    )
                    for item in customs.commodities
                ]
            )
            if payload.customs is not None else None
        ),
        CustomsContentType=(
            ContentType[customs.content_type or "other"].value
            if payload.customs is not None else None
        ),
        ContentComments=None,
        RestrictionType=None,
        RestrictionComments=None,
        AESITN=customs.aes,
        ImportersReference=None,
        ImportersContact=None,
        ExportersReference=None,
        ExportersContact=None,
        InvoiceNumber=customs.invoice,
        LicenseNumber=customs.license_number,
        CertificateNumber=customs.certificate_number,
        NonDeliveryOption=non_delivery,
        AltReturnAddress1=redirect_address.address_line1,
        AltReturnAddress2=redirect_address.address_line2,
        AltReturnAddress3=None,
        AltReturnAddress4=None,
        AltReturnAddress5=None,
        AltReturnAddress6=None,
        AltReturnCountry=None,
        LabelImportType=None,
        ChargebackCode=None,
        TrackingRetentionPeriod=None,
    )

    return Serializable(request, XP.export)
