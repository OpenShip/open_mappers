import time
from base64 import encodebytes
from typing import List, Tuple, Optional
from dhl_express_lib.ship_val_global_req_10_0 import (
    ShipmentRequest as DHLShipmentRequest,
    Billing,
    Consignee,
    Contact,
    Commodity,
    Shipper,
    ShipmentDetails as DHLShipmentDetails,
    Reference,
    Dutiable,
    MetaData,
    Notification,
    SpecialService,
    WeightType,
    Label,
    ExportDeclaration,
    ExportLineItem,
    AdditionalInformation,
)
from dhl_express_lib.ship_val_global_res_10_0 import LabelImage
from dhl_express_lib.datatypes_global_v10 import Pieces, Piece
from purplship.core.utils import Serializable, XP, SF, Location, Element
from purplship.core.models import (
    ShipmentRequest,
    Message,
    ShipmentDetails,
    Payment,
    Customs,
    Duty
)
from purplship.core.units import Options, Packages, CompleteAddress, Weight, WeightUnit
from purplship.providers.dhl_express.units import (
    PackageType,
    ProductCode,
    PaymentType,
    CountryRegion,
    SpecialServiceCode,
    DeliveryType,
    PackagePresets,
    LabelType,
    ExportReasonCode,
    WeightUnit as DHLWeightUnit,
    DimensionUnit,
    COUNTRY_PREFERED_UNITS,
)
from purplship.providers.dhl_express.utils import Settings
from purplship.providers.dhl_express.error import parse_error_response


UNSUPPORTED_PAPERLESS_COUNTRIES = ['JM']


def parse_shipment_response(
        response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    air_way_bill = XP.find("AirwayBillNumber", response, first=True)

    return (
        _extract_shipment(response, settings) if air_way_bill is not None else None,
        parse_error_response(response, settings),
    )


def _extract_shipment(shipment_node, settings: Settings) -> Optional[ShipmentDetails]:
    tracking_number = XP.find("AirwayBillNumber", shipment_node, first=True).text
    label_image = XP.find("LabelImage", shipment_node, LabelImage, first=True)
    label = encodebytes(label_image.OutputImage).decode("utf-8")

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        label=label,
    )


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[DHLShipmentRequest]:
    packages = Packages.map(payload.parcels, PackagePresets, required=["weight"])
    options = Options(payload.options, SpecialServiceCode)
    product = ProductCode.map(payload.service).value_or_key
    shipper = CompleteAddress.map(payload.shipper)
    recipient = CompleteAddress.map(payload.recipient)

    weight_unit, dim_unit = (COUNTRY_PREFERED_UNITS.get(payload.shipper.country_code) or packages.compatible_units)
    is_document = all(p.parcel.is_document for p in packages)
    package_type = PackageType[packages.package_type].value
    label_format, label_template = LabelType[payload.label_type or 'PDF_6x4'].value
    payment = (payload.payment or Payment(paid_by="sender", account_number=settings.account_number))
    customs = (payload.customs or Customs())
    is_dutiable = (is_document is False and customs.duty is not None)
    paperless_supported = (is_dutiable and payload.shipper.country_code not in UNSUPPORTED_PAPERLESS_COUNTRIES)
    duty = (customs.duty or Duty(paid_by="sender"))
    bill_to = CompleteAddress.map(duty.bill_to)
    content = (packages[0].parcel.content or customs.content_description or "N/A")
    reference = (payload.reference or getattr(payload, 'id', None))

    request = DHLShipmentRequest(
        schemaVersion='10.0',
        Request=settings.Request(
            MetaData=MetaData(SoftwareName="3PV", SoftwareVersion='10.0')
        ),
        RegionCode=CountryRegion[shipper.country_code].value,
        LanguageCode="en",
        LatinResponseInd=None,
        Billing=Billing(
            ShipperAccountNumber=settings.account_number,
            ShippingPaymentType=PaymentType[payment.paid_by].value,
            BillingAccountNumber=payment.account_number,
            DutyAccountNumber=duty.account_number,
        ),
        Consignee=Consignee(
            CompanyName=recipient.company_name or "N/A",
            SuiteDepartmentName=recipient.suite,
            AddressLine1=recipient.address_line1 or recipient.address_line,
            AddressLine2=SF.concat_str(recipient.address_line2, join=True),
            AddressLine3=None,
            City=recipient.city,
            Division=None,
            DivisionCode=recipient.state_code,
            PostalCode=recipient.postal_code,
            CountryCode=recipient.country_code,
            CountryName=recipient.country_name,
            Contact=Contact(
                PersonName=recipient.person_name,
                PhoneNumber=recipient.phone_number or "0000",
                Email=recipient.email,
            ),
            Suburb=recipient.suburb,
            StreetName=recipient.street_name,
            BuildingName=None,
            StreetNumber=recipient.street_number,
            RegistrationNumbers=None,
            BusinessPartyTypeCode=None,
        ),
        Commodity=(
            [
                Commodity(CommodityCode=c.sku, CommodityName=c.description)
                for c in payload.customs.commodities
            ]
            if any(customs.commodities) else None
        ),
        Dutiable=(
            Dutiable(
                DeclaredValue=duty.declared_value or options.declared_value or 1.0,
                DeclaredCurrency=duty.currency or options.currency or "USD",
                ScheduleB=None,
                ExportLicense=customs.license_number,
                ShipperEIN=None,
                ShipperIDType=None,
                TermsOfTrade=customs.incoterm,
                CommerceLicensed=None,
                Filing=None
            )
            if is_dutiable else None
        ),
        UseDHLInvoice=("Y" if is_dutiable else None),
        DHLInvoiceLanguageCode=("en" if is_dutiable else None),
        DHLInvoiceType=(("CMI" if customs.commercial_invoice else "PFI") if is_dutiable else None),
        ExportDeclaration=(
            ExportDeclaration(
                InterConsignee=None,
                IsPartiesRelation=None,
                ECCN=None,
                SignatureName=customs.signer,
                SignatureTitle=None,
                ExportReason=customs.content_type,
                ExportReasonCode=ExportReasonCode[customs.content_type or 'other'].value,
                SedNumber=None,
                SedNumberType=None,
                MxStateCode=None,
                InvoiceNumber=(customs.invoice or "N/A"),
                InvoiceDate=(customs.invoice_date or time.strftime("%Y-%m-%d")),
                BillToCompanyName=bill_to.company_name,
                BillToContactName=bill_to.person_name,
                BillToAddressLine=bill_to.address_line,
                BillToCity=bill_to.city,
                BillToPostcode=bill_to.postal_code,
                BillToSuburb=bill_to.extra,
                BillToCountryName=bill_to.country_name,
                BillToPhoneNumber=bill_to.phone_number,
                BillToPhoneNumberExtn=None,
                BillToFaxNumber=None,
                BillToFederalTaxID=bill_to.federal_tax_id,
                Remarks=customs.content_description,
                DestinationPort=None,
                TermsOfPayment=None,
                PayerGSTVAT=bill_to.state_tax_id,
                SignatureImage=None,
                ReceiverReference=None,
                ExporterId=None,
                ExporterCode=None,
                ExportLineItem=[
                    ExportLineItem(
                        LineNumber=index,
                        Quantity=item.quantity,
                        QuantityUnit='PCS',
                        Description=item.description or 'N/A',
                        Value=((item.quantity or 1) * (item.value_amount or 0.0)),
                        IsDomestic=None,
                        CommodityCode=item.sku,
                        ScheduleB=None,
                        ECCN=None,
                        Weight=WeightType(
                            Weight=Weight(item.weight, WeightUnit[item.weight_unit or 'KG'])[weight_unit.name],
                            WeightUnit=DHLWeightUnit[weight_unit.name].value
                        ),
                        GrossWeight=WeightType(
                            Weight=Weight(item.weight, WeightUnit[item.weight_unit or 'KG'])[weight_unit.name],
                            WeightUnit=DHLWeightUnit[weight_unit.name].value
                        ),
                        License=None,
                        LicenseSymbol=None,
                        ManufactureCountryCode=item.origin_country,
                        ManufactureCountryName=Location(item.origin_country).as_country_name,
                        ImportTaxManagedOutsideDhlExpress=None,
                        AdditionalInformation=None,
                        ImportCommodityCode=None,
                        ItemReferences=None,
                        CustomsPaperworks=None,
                    )
                    for (index, item) in enumerate(customs.commodities, start=1)
                ],
                ShipmentDocument=None,
                InvoiceInstructions=None,
                CustomerDataTextEntries=None,
                PlaceOfIncoterm="N/A",
                ShipmentPurpose=("COMMERCIAL" if customs.commercial_invoice else "PERSONAL"),
                DocumentFunction=None,
                CustomsDocuments=None,
                InvoiceTotalNetWeight=None,
                InvoiceTotalGrossWeight=None,
                InvoiceReferences=None,
            )
            if is_dutiable else None
        ),
        Reference=(
            [Reference(ReferenceID=reference)]
            if any([reference]) else None
        ),
        ShipmentDetails=DHLShipmentDetails(
            Pieces=Pieces(
                Piece=[
                    Piece(
                        PieceID=index,
                        PackageType=(
                            package_type or PackageType[package.packaging_type or "your_packaging"].value
                        ),
                        Depth=package.length[dim_unit.name],
                        Width=package.width[dim_unit.name],
                        Height=package.height[dim_unit.name],
                        Weight=package.weight[weight_unit.name],
                        PieceContents=(package.parcel.content or package.parcel.description),
                        PieceReference=(
                            [Reference(ReferenceID=package.parcel.id)]
                            if package.parcel.id is not None else None
                        ),
                        AdditionalInformation=(
                            AdditionalInformation(CustomerDescription=package.parcel.description)
                            if package.parcel.description is not None else None
                        )
                    )
                    for (index, package) in enumerate(packages, start=1)
                ]
            ),
            WeightUnit=DHLWeightUnit[weight_unit.name].value,
            GlobalProductCode=product,
            LocalProductCode=product,
            Date=(options.shipment_date or time.strftime("%Y-%m-%d")),
            Contents=content,
            DimensionUnit=DimensionUnit[dim_unit.name].value,
            PackageType=package_type,
            IsDutiable=("Y" if is_dutiable else "N"),
            CurrencyCode=options.currency or "USD",
            CustData=getattr(payload, 'id', None),
            ShipmentCharges=(options.cash_on_delivery if options.cash_on_delivery else None),
            ParentShipmentIdentificationNumber=None,
            ParentShipmentGlobalProductCode=None,
            ParentShipmentPackagesCount=None,
        ),
        Shipper=Shipper(
            ShipperID=settings.account_number or "N/A",
            CompanyName=shipper.company_name or "N/A",
            SuiteDepartmentName=shipper.suite,
            RegisteredAccount=settings.account_number,
            AddressLine1=shipper.address_line1 or shipper.address_line,
            AddressLine2=SF.concat_str(shipper.address_line2, join=True),
            AddressLine3=None,
            City=shipper.city,
            Division=None,
            DivisionCode=shipper.state_code,
            PostalCode=shipper.postal_code,
            OriginServiceAreaCode=None,
            OriginFacilityCode=None,
            CountryCode=shipper.country_code,
            CountryName=shipper.country_name,
            Contact=Contact(
                PersonName=shipper.person_name,
                PhoneNumber=shipper.phone_number or "0000",
                Email=shipper.email,
            ),
            Suburb=shipper.suburb,
            StreetName=shipper.street_name,
            BuildingName=None,
            StreetNumber=shipper.street_number,
            RegistrationNumbers=None,
            BusinessPartyTypeCode=None,
        ),
        SpecialService=(
            [
                SpecialService(
                    SpecialServiceType=SpecialServiceCode[key].value.key,
                    ChargeValue=getattr(svc, 'value', None),
                    CurrencyCode=(options.currency or "USD" if hasattr(svc, 'value') else None)
                )
                for key, svc in options if key in SpecialServiceCode
            ] +
            (  # Add paperless trade if dutiable
                [SpecialService(SpecialServiceType="WY")]
                if paperless_supported and 'dhl_paperless_trade' not in options else []
            )
        ),
        Notification=(
            Notification(EmailAddress=options.notification_email or recipient.email)
            if options.notification_email is None else None
        ),
        Place=None,
        EProcShip=None,
        Airwaybill=None,
        DocImages=None,
        LabelImageFormat=label_format,
        RequestArchiveDoc=None,
        NumberOfArchiveDoc=None,
        RequestQRCode='N',
        RequestTransportLabel=None,
        Label=Label(LabelTemplate=label_template),
        ODDLinkReq=None,
        DGs=None,
        GetPriceEstimate='Y',
        SinglePieceImage='N',
        ShipmentIdentificationNumber=None,
        UseOwnShipmentIdentificationNumber='N',
        Importer=None,
    )

    return Serializable(request, _request_serializer)


def _request_serializer(request: DHLShipmentRequest) -> str:
    xml_str = XP.export(
        request,
        name_="req:ShipmentRequest",
        namespacedef_='xsi:schemaLocation="http://www.dhl.com ship-val-global-req.xsd" xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
    ).replace('schemaVersion="10"', 'schemaVersion="10.0"')

    return xml_str
