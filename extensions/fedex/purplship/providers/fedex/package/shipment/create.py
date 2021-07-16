from datetime import datetime
from base64 import encodebytes
from typing import List, Tuple, cast
from fedex_lib.ship_service_v26 import (
    CompletedShipmentDetail,
    ProcessShipmentRequest,
    TransactionDetail,
    VersionId,
    RequestedShipment,
    RequestedPackageLineItem,
    Party,
    Contact,
    Address,
    TaxpayerIdentification,
    Weight as FedexWeight,
    Dimensions as FedexDimensions,
    CompletedPackageDetail,
    TrackingId,
    ShipmentSpecialServicesRequested,
    ShipmentEventNotificationDetail,
    ShipmentEventNotificationSpecification,
    NotificationDetail,
    EMailDetail,
    Localization,
    CodDetail,
    CodCollectionType,
    Money,
    ShippingDocumentPart,
    Payment,
    Payor,
    LabelSpecification,
    LabelFormatType,
    LabelPrintingOrientationType,
    ShipmentNotificationFormatSpecification,
    LabelOrderType,
    CustomsClearanceDetail,
    Commodity,
    CommercialInvoice,
    CustomerReference,
    CustomerReferenceType,
)
from purplship.core.utils import Serializable, apply_namespaceprefix, create_envelope, Element, SF, XP, DF
from purplship.core.units import Options, Packages, CompleteAddress, Weight
from purplship.core.models import ShipmentDetails, Message, ShipmentRequest
from purplship.providers.fedex.error import parse_error_response
from purplship.providers.fedex.utils import Settings
from purplship.providers.fedex.units import (
    PackagingType,
    ServiceType,
    SpecialServiceType,
    PackagePresets,
    PaymentType,
    LabelType,
    Incoterm,
    PurposeType,
    MeasurementOptions,
)


NOTIFICATION_EVENTS = [
    "ON_DELIVERY",
    "ON_ESTIMATED_DELIVERY",
    "ON_EXCEPTION",
    "ON_SHIPMENT",
    "ON_TENDER",
]


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    detail = XP.find("CompletedShipmentDetail", response, first=True)
    shipment = (
        _extract_shipment(detail, settings) if detail is not None else None
    )
    return shipment, parse_error_response(response, settings)


def _extract_shipment(
    shipment_detail_node: Element, settings: Settings
) -> ShipmentDetails:
    detail = XP.build(CompletedShipmentDetail, shipment_detail_node)

    tracking_number = cast(TrackingId, detail.MasterTrackingId).TrackingNumber
    package: CompletedPackageDetail = next(iter(detail.CompletedPackageDetails), None)
    part: ShippingDocumentPart = (
        next(iter(package.Label.Parts)) if package is not None else None
    )
    label = (
        encodebytes(cast(ShippingDocumentPart, part).Image).decode("utf-8")
        if part is not None
        else None
    )

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        label=label,
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[ProcessShipmentRequest]:
    shipper = CompleteAddress.map(payload.shipper)
    recipient = CompleteAddress.map(payload.recipient)
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])
    # Only the master package is selected here because even for MPS only one package is accepted for a master tracking.
    master_package = packages[0]

    service = ServiceType.map(payload.service).value_or_key
    options = Options(payload.options, SpecialServiceType)
    special_services = [getattr(v, 'value', v) for k, v in options if k in SpecialServiceType]
    label_type, label_format = LabelType[payload.label_type or 'PDF_4x6'].value
    customs = payload.customs
    duty = customs.duty if customs is not None else None
    bill_to = CompleteAddress(getattr(duty, 'bill_to', None))

    request = ProcessShipmentRequest(
        WebAuthenticationDetail=settings.webAuthenticationDetail,
        ClientDetail=settings.clientDetail,
        TransactionDetail=TransactionDetail(CustomerTransactionId="IE_v26_Ship"),
        Version=VersionId(ServiceId="ship", Major=26, Intermediate=0, Minor=0),
        RequestedShipment=RequestedShipment(
            ShipTimestamp=DF.date(options.shipment_date or datetime.now()),
            DropoffType="REGULAR_PICKUP",
            ServiceType=service,
            PackagingType=PackagingType[packages.package_type or 'your_packaging'].value,
            ManifestDetail=None,
            VariationOptions=None,
            TotalWeight=FedexWeight(
                Units=packages.weight.unit,
                Value=packages.weight.value
            ),
            TotalInsuredValue=options.insurance,
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
            ShippingChargesPayment=Payment(
                PaymentType=PaymentType[payload.payment.paid_by or "sender"].value,
                Payor=Payor(
                    ResponsibleParty=Party(
                        AccountNumber=(payload.payment.account_number or settings.account_number),
                    )
                ),
            ),
            SpecialServicesRequested=(
                ShipmentSpecialServicesRequested(
                    SpecialServiceTypes=special_services,
                    CodDetail=(
                        CodDetail(
                            CodCollectionAmount=Money(
                                Currency=options.currency or "USD",
                                Amount=options.cash_on_delivery,
                            ),
                            AddTransportationChargesDetail=None,
                            CollectionType=CodCollectionType.CASH,
                            CodRecipient=None,
                            FinancialInstitutionContactAndAddress=None,
                            RemitToName=None,
                            ReferenceIndicator=None,
                            ReturnTrackingId=None,
                        )
                        if options.cash_on_delivery else None
                    ),
                    DeliveryOnInvoiceAcceptanceDetail=None,
                    HoldAtLocationDetail=None,
                    EventNotificationDetail=(
                        ShipmentEventNotificationDetail(
                            AggregationType=None,
                            PersonalMessage=None,
                            EventNotifications=[
                                ShipmentEventNotificationSpecification(
                                    Role=None,
                                    Events=NOTIFICATION_EVENTS,
                                    NotificationDetail=NotificationDetail(
                                        NotificationType="EMAIL",
                                        EmailDetail=EMailDetail(
                                            EmailAddress=options.notification_email or recipient.email,
                                            Name=recipient.person_name or recipient.company_name,
                                        ),
                                        Localization=Localization(LanguageCode="EN"),
                                    ),
                                    FormatSpecification=ShipmentNotificationFormatSpecification(
                                        Type="TEXT"
                                    ),
                                )
                            ],
                        )
                        if options.notification_email is None else None
                    ),
                    ReturnShipmentDetail=None,
                    PendingShipmentDetail=None,
                    InternationalControlledExportDetail=None,
                    InternationalTrafficInArmsRegulationsDetail=None,
                    ShipmentDryIceDetail=None,
                    HomeDeliveryPremiumDetail=None,
                    EtdDetail=None,
                )
                if options.has_content else None
            ),
            ExpressFreightDetail=None,
            FreightShipmentDetail=None,
            DeliveryInstructions=None,
            VariableHandlingChargeDetail=None,
            CustomsClearanceDetail=(
                CustomsClearanceDetail(
                    Brokers=None,
                    ClearanceBrokerage=None,
                    CustomsOptions=None,
                    ImporterOfRecord=None,
                    RecipientCustomsId=None,
                    DutiesPayment=(
                        Payment(
                            PaymentType=PaymentType[duty.paid_by or "sender"].value,
                            Payor=(
                                Payor(
                                    ResponsibleParty=Party(
                                        AccountNumber=duty.account_number,
                                        Tins=bill_to.taxes
                                    )
                                ) if any([duty.account_number, bill_to.taxes]) else None
                            )
                        ) if duty is not None else None
                    ),
                    DocumentContent=None,
                    CustomsValue=Money(
                        Currency=(duty.currency or options.currency),
                        Amount=(duty.declared_value or options.declared_value)
                    ),
                    FreightOnValue=None,
                    InsuranceCharges=None,
                    PartiesToTransactionAreRelated=None,
                    CommercialInvoice=(
                        CommercialInvoice(
                            Comments=None,
                            FreightCharge=None,
                            TaxesOrMiscellaneousChargeType=None,
                            PackingCosts=None,
                            HandlingCosts=None,
                            SpecialInstructions=None,
                            DeclarationStatement=None,
                            PaymentTerms=None,
                            Purpose=PurposeType[customs.content_type or 'other'].value,
                            PurposeOfShipmentDescription=None,
                            CustomerReferences=None,
                            OriginatorName=(shipper.company_name or shipper.person_name),
                            TermsOfSale=Incoterm[customs.incoterm or "DDU"].value
                        )
                        if customs.commercial_invoice else None
                    ),
                    Commodities=[
                        Commodity(
                            Name=None,
                            NumberOfPieces=item.quantity,
                            Description=item.description or "N/A",
                            Purpose=None,
                            CountryOfManufacture=item.origin_country,
                            HarmonizedCode=None,
                            Weight=FedexWeight(
                                Units=master_package.weight_unit.value,
                                Value=Weight(item.weight, item.weight_unit)[master_package.weight_unit.value]
                            ),
                            Quantity=item.quantity,
                            QuantityUnits='EA',
                            AdditionalMeasures=None,
                            UnitPrice=Money(
                                Currency=(options.currency or duty.currency),
                                Amount=item.value_amount,
                            ),
                            CustomsValue=None,
                            ExciseConditions=None,
                            ExportLicenseNumber=None,
                            ExportLicenseExpirationDate=None,
                            CIMarksAndNumbers=None,
                            PartNumber=item.sku,
                            NaftaDetail=None,
                        ) for item in customs.commodities
                    ],
                    ExportDetail=None,
                    RegulatoryControls=None,
                    DeclarationStatementDetail=None
                ) if payload.customs is not None else None
            ),
            PickupDetail=None,
            SmartPostDetail=None,
            BlockInsightVisibility=None,
            LabelSpecification=LabelSpecification(
                Dispositions=None,
                LabelFormatType=LabelFormatType.COMMON_2_D.value,
                ImageType=label_type,
                LabelStockType=label_format,
                LabelPrintingOrientation=LabelPrintingOrientationType.TOP_EDGE_OF_TEXT_FIRST.value,
                LabelOrder=LabelOrderType.SHIPPING_LABEL_FIRST.value,
                PrintedLabelOrigin=None,
                CustomerSpecifiedDetail=None,
            ),
            ShippingDocumentSpecification=None,
            RateRequestTypes=None,
            EdtRequestType=None,
            MasterTrackingId=None,
            PackageCount=len(packages),
            ConfigurationData=None,
            RequestedPackageLineItems=[
                RequestedPackageLineItem(
                    SequenceNumber=1,
                    GroupNumber=None,
                    GroupPackageCount=None,
                    VariableHandlingChargeDetail=None,
                    InsuredValue=None,
                    Weight=(
                        FedexWeight(
                            Units=master_package.weight.unit,
                            Value=master_package.weight.value,
                        )
                        if master_package.weight.value else None
                    ),
                    Dimensions=(
                        FedexDimensions(
                            Length=master_package.length.map(MeasurementOptions).value,
                            Width=master_package.width.map(MeasurementOptions).value,
                            Height=master_package.height.map(MeasurementOptions).value,
                            Units=master_package.dimension_unit.value,
                        )
                        if master_package.has_dimensions else None
                    ),
                    PhysicalPackaging=None,
                    ItemDescription=master_package.parcel.description,
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
            ],
        ),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: ProcessShipmentRequest) -> str:
    namespacedef_ = 'xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v26="http://fedex.com/ws/ship/v26"'

    envelope = create_envelope(body_content=request)
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "v26")

    return XP.export(envelope, namespacedef_=namespacedef_)
