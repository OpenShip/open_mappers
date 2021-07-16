from functools import partial
from typing import List, Tuple, cast, Union, Type
from purolator_lib.shipping_documents_service_1_3_0 import DocumentDetail
from purolator_lib.shipping_service_2_1_3 import (
    CreateShipmentRequest,
    CreateShipmentResponse,
    PIN,
    Shipment,
    SenderInformation,
    ReceiverInformation,
    PackageInformation,
    TrackingReferenceInformation,
    Address,
    InternationalInformation,
    PickupInformation,
    PickupType,
    ArrayOfPiece,
    Piece,
    Weight as PurolatorWeight,
    WeightUnit as PurolatorWeightUnit,
    RequestContext,
    Dimension as PurolatorDimension,
    DimensionUnit as PurolatorDimensionUnit,
    TotalWeight,
    PhoneNumber,
    PaymentInformation,
    DutyInformation,
    NotificationInformation,
    ArrayOfOptionIDValuePair,
    OptionIDValuePair,
    BusinessRelationship,
    PrinterType,
    ContentDetail,
    ArrayOfContentDetail,
)
from purplship.core.units import Options, Packages, Phone
from purplship.core.utils import (
    Serializable, Element, create_envelope, Pipeline, Job, Envelope, XP, SF
)
from purplship.core.models import ShipmentRequest, ShipmentDetails, Message

from purplship.providers.purolator.shipment.documents import get_shipping_documents_request
from purplship.providers.purolator.utils import Settings, standard_request_serializer
from purplship.providers.purolator.error import parse_error_response
from purplship.providers.purolator.units import (
    Product,
    Service,
    PackagePresets,
    PaymentType,
    DutyPaymentType,
    MeasurementOptions,
    PrintType,
    NON_OFFICIAL_SERVICES,
)


def parse_shipment_response(
        response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    details = XP.find("CreateShipmentResponse", response, first=True)
    shipment = _extract_shipment(response, settings) if details is not None else None
    return shipment, parse_error_response(response, settings)


def _extract_shipment(response: Element, settings: Settings) -> ShipmentDetails:
    shipment = XP.find("CreateShipmentResponse", response, CreateShipmentResponse, first=True)
    document = XP.find("DocumentDetail", response, DocumentDetail, first=True) or DocumentDetail()

    pin = cast(PIN, shipment.ShipmentPIN).Value

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=pin,
        shipment_identifier=pin,
        label=document.Data,
    )


def shipment_request(
        payload: ShipmentRequest, settings: Settings
) -> Serializable[Pipeline]:
    requests: Pipeline = Pipeline(
        create=lambda *_: partial(_create_shipment, payload=payload, settings=settings)(),
        document=partial(_get_shipment_label, payload=payload, settings=settings),
    )
    return Serializable(requests)


def _shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[Envelope]:
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])
    service = Product.map(payload.service).value_or_key
    options = Options(payload.options, Service)

    is_document = all([parcel.is_document for parcel in payload.parcels])
    package_description = packages[0].parcel.description if len(packages) == 1 else None
    is_international = (payload.shipper.country_code != payload.recipient.country_code)
    shipper_phone_number = Phone(payload.shipper.phone_number, payload.shipper.country_code)
    recipient_phone_number = Phone(payload.recipient.phone_number, payload.recipient.country_code)
    printing = PrintType.map(payload.label_type or "PDF").value
    option_ids = [
        (key, value) for key, value in options if key in Service and key not in NON_OFFICIAL_SERVICES
    ]

    request = create_envelope(
        header_content=RequestContext(
            Version="2.1",
            Language=settings.language,
            GroupID="",
            RequestReference=(getattr(payload, 'id', None) or ""),
            UserToken=settings.user_token,
        ),
        body_content=CreateShipmentRequest(
            Shipment=Shipment(
                SenderInformation=SenderInformation(
                    Address=Address(
                        Name=payload.shipper.person_name,
                        Company=payload.shipper.company_name,
                        Department=None,
                        StreetNumber="",
                        StreetSuffix=None,
                        StreetName=SF.concat_str(payload.shipper.address_line1, join=True),
                        StreetType=None,
                        StreetDirection=None,
                        Suite=None,
                        Floor=None,
                        StreetAddress2=SF.concat_str(payload.shipper.address_line2, join=True),
                        StreetAddress3=None,
                        City=payload.shipper.city or "",
                        Province=payload.shipper.state_code or "",
                        Country=payload.shipper.country_code or "",
                        PostalCode=payload.shipper.postal_code or "",
                        PhoneNumber=PhoneNumber(
                            CountryCode=shipper_phone_number.country_code or "0",
                            AreaCode=shipper_phone_number.area_code or "0",
                            Phone=shipper_phone_number.phone or "0",
                            Extension=None,
                        ),
                        FaxNumber=None,
                    ),
                    TaxNumber=(payload.shipper.federal_tax_id or payload.shipper.state_tax_id),
                ),
                ReceiverInformation=ReceiverInformation(
                    Address=Address(
                        Name=payload.recipient.person_name,
                        Company=payload.recipient.company_name,
                        Department=None,
                        StreetNumber="",
                        StreetSuffix=None,
                        StreetName=SF.concat_str(payload.recipient.address_line1, join=True),
                        StreetType=None,
                        StreetDirection=None,
                        Suite=None,
                        Floor=None,
                        StreetAddress2=SF.concat_str(payload.recipient.address_line2, join=True),
                        StreetAddress3=None,
                        City=payload.recipient.city or "",
                        Province=payload.recipient.state_code or "",
                        Country=payload.recipient.country_code or "",
                        PostalCode=payload.recipient.postal_code or "",
                        PhoneNumber=PhoneNumber(
                            CountryCode=recipient_phone_number.country_code or "0",
                            AreaCode=recipient_phone_number.area_code or "0",
                            Phone=recipient_phone_number.phone or "0",
                            Extension=None,
                        ),
                        FaxNumber=None,
                    ),
                    TaxNumber=(payload.recipient.federal_tax_id or payload.recipient.state_tax_id),
                ),
                FromOnLabelIndicator=None,
                FromOnLabelInformation=None,
                ShipmentDate=options.shipment_date,
                PackageInformation=PackageInformation(
                    ServiceID=service,
                    Description=package_description,
                    TotalWeight=(
                        TotalWeight(
                            Value=packages.weight.map(MeasurementOptions).LB,
                            WeightUnit=PurolatorWeightUnit.LB.value,
                        ) if packages.weight.value else None
                    ),
                    TotalPieces=1,
                    PiecesInformation=ArrayOfPiece(
                        Piece=[
                            Piece(
                                Weight=(
                                    PurolatorWeight(
                                        Value=package.weight.map(MeasurementOptions).value,
                                        WeightUnit=PurolatorWeightUnit[
                                            package.weight_unit.value
                                        ].value,
                                    )
                                    if package.weight.value else None
                                ),
                                Length=(
                                    PurolatorDimension(
                                        Value=package.length.map(MeasurementOptions).value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.length.value else None
                                ),
                                Width=(
                                    PurolatorDimension(
                                        Value=package.width.map(MeasurementOptions).value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.width.value else None
                                ),
                                Height=(
                                    PurolatorDimension(
                                        Value=package.height.map(MeasurementOptions).value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.height.value else None
                                ),
                                Options=None,
                            )
                            for package in packages
                        ]
                    ),
                    DangerousGoodsDeclarationDocumentIndicator=None,
                    OptionsInformation=(
                        ArrayOfOptionIDValuePair(
                            OptionIDValuePair=[
                                OptionIDValuePair(ID=key, Value=value)
                                for key, value in option_ids
                            ]
                        )
                        if any(option_ids) else None
                    ),
                ),
                InternationalInformation=(
                    InternationalInformation(
                        DocumentsOnlyIndicator=is_document,
                        ContentDetails=(
                            ArrayOfContentDetail(
                                ContentDetail=[
                                    ContentDetail(
                                        Description=c.description,
                                        HarmonizedCode=None,
                                        CountryOfManufacture=c.origin_country,
                                        ProductCode=c.sku,
                                        UnitValue=c.value_amount,
                                        Quantity=c.quantity,
                                        NAFTADocumentIndicator=None,
                                        FDADocumentIndicator=None,
                                        FCCDocumentIndicator=None,
                                        SenderIsProducerIndicator=None,
                                        TextileIndicator=None,
                                        TextileManufacturer=None,
                                    )
                                    for c in payload.customs.commodities
                                ]
                            ) if not is_document else None
                        ),
                        BuyerInformation=None,
                        PreferredCustomsBroker=None,
                        DutyInformation=(
                            DutyInformation(
                                BillDutiesToParty=DutyPaymentType[
                                    payload.customs.duty.paid_by
                                ].value,
                                BusinessRelationship=BusinessRelationship.NOT_RELATED.value,
                                Currency=payload.customs.duty.currency,
                            ) if payload.customs is not None else None
                        ),
                        ImportExportType=None,
                        CustomsInvoiceDocumentIndicator=None,
                    )
                    if is_international else None
                ),
                ReturnShipmentInformation=None,
                PaymentInformation=(
                    PaymentInformation(
                        PaymentType=PaymentType[payload.payment.paid_by].value,
                        RegisteredAccountNumber=(payload.payment.account_number or settings.account_number),
                        BillingAccountNumber=(payload.payment.account_number or settings.account_number),
                        CreditCardInformation=None,
                    )
                    if payload.payment is not None else None
                ),
                PickupInformation=PickupInformation(
                    PickupType=PickupType.DROP_OFF.value
                ),
                NotificationInformation=(
                    NotificationInformation(
                        ConfirmationEmailAddress=(options.notification_email or payload.recipient.email)
                    )
                    if any([options.notification_email or payload.recipient.email]) else None
                ),
                TrackingReferenceInformation=(
                    TrackingReferenceInformation(Reference1=payload.reference)
                    if payload.reference != "" else None
                ),
                OtherInformation=None,
                ProactiveNotification=None,
            ),
            PrinterType=PrinterType(printing).value,
        ),
    )
    return Serializable(request, standard_request_serializer)


def _create_shipment(payload: ShipmentRequest, settings: Settings) -> Job:
    return Job(
        id="create",
        data=_shipment_request(payload, settings),
    )


def _get_shipment_label(create_response: str, payload: ShipmentRequest, settings: Settings) -> Job:
    response = XP.to_xml(create_response)
    valid = len(parse_error_response(response, settings)) == 0
    shipment_pin = (
        getattr(XP.find("ShipmentPIN", response, PIN, first=True), 'Value', None)
        if valid else None
    )
    data = (
        get_shipping_documents_request(shipment_pin, payload, settings)
        if valid else None
    )

    return Job(id="document", data=data, fallback="")
