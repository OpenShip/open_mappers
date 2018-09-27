from typing import List, Tuple, TypeVar
from functools import reduce
import time
from purplship.domain import entities as E
from purplship.domain.mapper import Mapper
from purplship.mappers.dhl.dhl_client import DHLClient
from pydhl import DCT_req_global as Req, DCT_Response_global as Res, tracking_request_known as Track, tracking_response as TrackRes
from pydhl.datatypes_global_v61 import ServiceHeader, MetaData, Request
from pydhl import ship_val_global_req_61 as ShipReq
from gds_helpers import jsonify_xml, jsonify
from lxml import etree

class DHLMapper(Mapper):
    def __init__(self, client: DHLClient):
        self.client = client

    """ Shared functions """

    def init_request(self) -> Request:
        ServiceHeader_ = ServiceHeader(
            MessageReference="1234567890123456789012345678901",
            MessageTime=time.strftime('%Y-%m-%dT%H:%M:%S'),
            SiteID=self.client.site_id,
            Password=self.client.password
        )
        return Request(ServiceHeader=ServiceHeader_)

    def parse_error_response(self, response) -> List[E.Error]:
        conditions = response.xpath(
            './/*[local-name() = $name]', name="Condition")
        return reduce(self._extract_error, conditions, [])

    """ Interface functions """

    def create_quote_request(self, payload: E.quote_request) -> Req.DCTRequest:
        Request_ = self.init_request()
        Request_.MetaData = MetaData(SoftwareName="3PV", SoftwareVersion="1.0")

        From_ = Req.DCTFrom(
            CountryCode=payload.shipper.country_code,
            Postalcode=payload.shipper.postal_code,
            City=payload.shipper.city,
            Suburb=payload.shipper.state_code
        )

        To_ = Req.DCTTo(
            CountryCode=payload.recipient.country_code,
            Postalcode=payload.recipient.postal_code,
            City=payload.recipient.city,
            Suburb=payload.recipient.state_code
        )

        Pieces = Req.PiecesType()
        for p in payload.shipment.packages:
            Pieces.add_Piece(Req.PieceType(
                PieceID=p.id,
                PackageTypeCode=p.packaging_type or "BOX",
                Height=p.height, Width=p.width,
                Weight=p.weight, Depth=p.length
            ))

        payment_country_code = "CA" if not payload.shipment.payment_country_code else payload.shipment.payment_country_code

        BkgDetails_ = Req.BkgDetailsType(
            PaymentCountryCode=payment_country_code,
            NetworkTypeCode="AL",
            WeightUnit=payload.shipment.weight_unit or "LB",
            DimensionUnit=payload.shipment.dimension_unit or "IN",
            ReadyTime=time.strftime("PT%HH%MM"),
            Date=time.strftime("%Y-%m-%d"),
            PaymentAccountNumber=self.client.account_number,
            IsDutiable="N" if payload.shipment.is_document else "Y",
            Pieces=Pieces
        )

        GetQuote = Req.GetQuoteType(
            Request=Request_, From=From_, To=To_, BkgDetails=BkgDetails_)

        return Req.DCTRequest(schemaVersion="1.0", GetQuote=GetQuote)

    def create_shipment_request(self, payload: E.shipment_request) ->ShipReq.ShipmentRequest:
        Request_ = self.init_request()
        Request_.MetaData = MetaData(SoftwareName="3PV", SoftwareVersion="1.0")

        Billing_ = ShipReq.Billing(
            ShipperAccountNumber=payload.shipment.shipper_account_number or self.client.account_number,
            BillingAccountNumber=payload.shipment.payment_account_number,
            ShippingPaymentType=payload.shipment.paid_by,
            DutyAccountNumber=payload.shipment.duty_payment_account,
            DutyPaymentType=payload.shipment.duty_paid_by
        )

        Consignee_ = ShipReq.Consignee(
            CompanyName=payload.recipient.company_name,
            PostalCode=payload.recipient.postal_code,
            CountryCode=payload.recipient.country_code,
            City=payload.recipient.city,
            CountryName=payload.recipient.country_name,
            Division=payload.recipient.state,
            DivisionCode=payload.recipient.state_code
        )

        if any([payload.recipient.person_name, payload.recipient.email_address]):
            Consignee_.Contact = ShipReq.Contact(
                PersonName=payload.recipient.person_name,
                PhoneNumber=payload.recipient.phone_number,
                Email=payload.recipient.email_address,
                FaxNumber=payload.recipient.extra.get('FaxNumber'),
                Telex=payload.recipient.extra.get('Telex'),
                PhoneExtension=payload.recipient.extra.get('PhoneExtension'),
                MobilePhoneNumber=payload.recipient.extra.get('MobilePhoneNumber')
            )

        [Consignee_.add_AddressLine(line)
         for line in payload.recipient.address_lines]

        Shipper_ = ShipReq.Shipper(
            ShipperID=payload.shipment.extra.get('ShipperID') or Billing_.ShipperAccountNumber,
            RegisteredAccount=payload.shipment.extra.get('ShipperID') or Billing_.ShipperAccountNumber,
            CompanyName=payload.shipper.company_name,
            PostalCode=payload.shipper.postal_code,
            CountryCode=payload.shipper.country_code,
            City=payload.shipper.city,
            CountryName=payload.shipper.country_name,
            Division=payload.shipper.state,
            DivisionCode=payload.shipper.state_code
        )

        if any([payload.shipper.person_name, payload.shipper.email_address]):
            Shipper_.Contact = ShipReq.Contact(
                PersonName=payload.shipper.person_name,
                PhoneNumber=payload.shipper.phone_number,
                Email=payload.shipper.email_address,
                FaxNumber=payload.shipper.extra.get('FaxNumber'),
                Telex=payload.shipper.extra.get('Telex'),
                PhoneExtension=payload.shipper.extra.get('PhoneExtension'),
                MobilePhoneNumber=payload.shipper.extra.get('MobilePhoneNumber')
            )

        [Shipper_.add_AddressLine(line)
         for line in payload.shipper.address_lines]

        Pieces_ = ShipReq.Pieces()
        for p in payload.shipment.packages:
            Pieces_.add_Piece(ShipReq.Piece(
                PieceID=p.id,
                PackageType=p.packaging_type,
                Weight=p.weight,
                DimWeight=p.extra.get('DimWeight'),
                Height=p.height,
                Width=p.width,
                Depth=p.length,
                PieceContents=p.description
            ))

        """ 
            Get PackageType from extra when implementing multi carrier,
            Get weight from total_weight if specified otherwise calculated from packages weight sum
        """
        ShipmentDetails_ = ShipReq.ShipmentDetails(
            NumberOfPieces=len(payload.shipment.packages),
            Pieces=Pieces_,
            Weight=payload.shipment.total_weight or sum([p.weight for p in payload.shipment.packages]),
            CurrencyCode=payload.shipment.currency or "USD",
            WeightUnit=(payload.shipment.weight_unit or "LB")[0],
            DimensionUnit=(payload.shipment.dimension_unit or "IN")[0],
            Date=payload.shipment.date or time.strftime('%Y-%m-%d'),
            PackageType=payload.shipment.packaging_type or payload.shipment.extra.get('PackageType'),
            IsDutiable= "N" if payload.shipment.is_document else "Y",
            InsuredAmount=payload.shipment.insured_amount,
            DoorTo=payload.shipment.extra.get('DoorTo'),
            GlobalProductCode=payload.shipment.extra.get('GlobalProductCode'),
            LocalProductCode=payload.shipment.extra.get('LocalProductCode'),
            Contents=payload.shipment.extra.get('Contents') or ""
        )

        ShipmentRequest_ = ShipReq.ShipmentRequest(
            schemaVersion="6.1",
            Request=Request_,
            RegionCode="AM",
            RequestedPickupTime="Y",
            LanguageCode="en",
            PiecesEnabled="Y",
            Billing=Billing_,
            Consignee=Consignee_,
            Shipper=Shipper_,
            ShipmentDetails=ShipmentDetails_,
            EProcShip=payload.shipment.extra.get('EProcShip')
        )

        if payload.shipment.label is not None:
            DocImages_ = ShipReq.DocImages()
            DocImages_.add_DocImage(ShipReq.DocImage(
                Type=payload.shipment.label.type,
                ImageFormat=payload.shipment.label.format,
                Image=payload.shipment.label.extra.get('Image')
            ))
            ShipmentRequest_.DocImages = DocImages_

        if ShipmentDetails_.IsDutiable == "Y":
            ShipmentRequest_.Dutiable = ShipReq.Dutiable(
                DeclaredCurrency=ShipmentDetails_.CurrencyCode,
                DeclaredValue=payload.shipment.declared_value,
                TermsOfTrade=payload.shipment.customs.terms_of_trade,
                ScheduleB=payload.shipment.customs.extra.get('ScheduleB'),
                ExportLicense=payload.shipment.customs.extra.get('ExportLicense'),
                ShipperEIN=payload.shipment.customs.extra.get('ShipperEIN'),
                ShipperIDType=payload.shipment.customs.extra.get('ShipperIDType'),
                ImportLicense=payload.shipment.customs.extra.get('ImportLicense'),
                ConsigneeEIN=payload.shipment.customs.extra.get('ConsigneeEIN')
            )

        [ShipmentRequest_.add_SpecialService(
            ShipReq.SpecialService(SpecialServiceType=service)
        ) for service in payload.shipment.services]

        [ShipmentRequest_.add_Commodity(
            ShipReq.Commodity(CommodityCode=c.code, CommodityName=c.description)
        ) for c in payload.shipment.commodities]

        [ShipmentRequest_.add_Reference(
            ShipReq.Reference(ReferenceID=r)
        ) for r in payload.shipment.references]

        return ShipmentRequest_

    def create_tracking_request(self, payload: E.tracking_request) -> Track.KnownTrackingRequest:
        known_request = Track.KnownTrackingRequest(
            Request=self.init_request(),
            LanguageCode=payload.language_code or "en",
            LevelOfDetails=payload.level_of_details or "ALL_CHECK_POINTS"
        )
        for tn in payload.tracking_numbers:
            known_request.add_AWBNumber(tn)
        return known_request

    def parse_quote_response(self, response) -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        qtdshp_list = response.xpath(
            './/*[local-name() = $name]', name="QtdShp")
        quotes = reduce(self._extract_quote, qtdshp_list, [])
        return (quotes, self.parse_error_response(response))

    def parse_tracking_response(self, response) -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        awbinfos = response.xpath('.//*[local-name() = $name]', name="AWBInfo")
        trackings = reduce(self._extract_tracking, awbinfos, [])
        return (trackings, self.parse_error_response(response))

    def parse_shipment_response(self, response) -> Tuple[E.ShipmentDetails, List[E.Error]]:
        AirwayBillNumber = response.xpath("//AirwayBillNumber")
        shipment = self._extract_shipment(response) if len(AirwayBillNumber) == 1 else None
        return (shipment, self.parse_error_response(response))

    """ Helpers functions """

    def _extract_error(self, errors: List[E.Error], conditionNode) -> List[E.Error]:
        condition = Res.ConditionType()
        condition.build(conditionNode)
        return errors + [
            E.Error(code=condition.ConditionCode,
                    message=condition.ConditionData, carrier=self.client.carrier_name)
        ]

    def _extract_quote(self, quotes: List[E.QuoteDetails], qtdshpNode) -> List[E.QuoteDetails]:
        qtdshp = Res.QtdShpType()
        qtdshp.build(qtdshpNode)
        ExtraCharges = list(map(lambda s: E.ChargeDetails(
            name=s.LocalServiceTypeName, amount=float(s.ChargeValue or 0)), qtdshp.QtdShpExChrg))
        Discount_ = reduce(
            lambda d, ec: d + ec.value if "Discount" in ec.name else d, ExtraCharges, 0)
        DutiesAndTaxes_ = reduce(
            lambda d, ec: d + ec.value if "TAXES PAID" in ec.name else d, ExtraCharges, 0)
        return quotes + [
            E.QuoteDetails(
                carrier=self.client.carrier_name,
                currency=qtdshp.CurrencyCode,
                delivery_date=str(qtdshp.DeliveryDate[0].DlvyDateTime),
                pickup_date=str(qtdshp.PickupDate),
                pickup_time=str(qtdshp.PickupCutoffTime),
                service_name=qtdshp.LocalProductName,
                service_type=qtdshp.NetworkTypeCode,
                base_charge=float(qtdshp.WeightCharge or 0),
                total_charge=float(qtdshp.ShippingCharge or 0),
                duties_and_taxes=DutiesAndTaxes_,
                discount=Discount_,
                extra_charges=list(map(lambda s: E.ChargeDetails(
                    name=s.LocalServiceTypeName, amount=float(s.ChargeValue or 0)), qtdshp.QtdShpExChrg))
            )
        ]

    def _extract_tracking(self, trackings: List[E.TrackingDetails], awbInfoNode) -> List[E.TrackingDetails]:
        awbInfo = TrackRes.AWBInfo()
        awbInfo.build(awbInfoNode)
        if awbInfo.ShipmentInfo == None:
            return trackings
        return trackings + [
            E.TrackingDetails(
                carrier=self.client.carrier_name,
                tracking_number=awbInfo.AWBNumber,
                shipment_date=str(awbInfo.ShipmentInfo.ShipmentDate),
                events=list(map(lambda e: E.TrackingEvent(
                    date=str(e.Date),
                    time=str(e.Time),
                    signatory=e.Signatory,
                    code=e.ServiceEvent.EventCode,
                    location=e.ServiceArea.Description,
                    description=e.ServiceEvent.Description
                ), awbInfo.ShipmentInfo.ShipmentEvent))
            )
        ]

    def _extract_shipment(self, shipmentResponseNode) -> E.ShipmentDetails:
        """
            Shipment extraction is implemented using lxml queries instead of generated ShipmentResponse type
            because the type construction fail during validation out of our control
        """
        get_value = lambda query: query[0].text if len(query) > 0 else None
        get = lambda key: get_value(shipmentResponseNode.xpath("//%s" % key))
        plates = [p.text for p in shipmentResponseNode.xpath("//LicensePlateBarCode")]
        barcodes = [child.text for child in shipmentResponseNode.xpath("//Barcodes")[0].getchildren()]
        documents = reduce(lambda r,i: (r + [i] if i else r), [get("AWBBarCode")] + plates + barcodes, [])
        reference = E.ReferenceDetails(value=get("ReferenceID"), type=get("ReferenceType")) if len(shipmentResponseNode.xpath("//Reference")) > 0 else None
        return E.ShipmentDetails(
            carrier=self.client.carrier_name,
            tracking_number = get("AirwayBillNumber"),
            shipment_date= get("ShipmentDate"),
            service=get("ProductShortName"),
            documents=documents,
            reference=reference,
            total_charge= E.ChargeDetails(name="Shipment charge", amount=get("ShippingCharge"), currency=get("CurrencyCode"))
        )