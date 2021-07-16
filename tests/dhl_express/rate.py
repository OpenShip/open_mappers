import re
import unittest
from unittest.mock import patch
from purplship.core.utils import DP
from purplship.core.models import RateRequest
from purplship import Rating
from tests.dhl_express.fixture import gateway


class TestDHLRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        # remove MessageTime, Date and ReadyTime for testing purpose
        serialized_request = re.sub(
            "<MessageTime>[^>]+</MessageTime>",
            "",
            re.sub(
                "<Date>[^>]+</Date>",
                "",
                re.sub("<ReadyTime>[^>]+</ReadyTime>", "", request.serialize()),
            ),
        )

        self.assertEqual(serialized_request, RateRequestXML)

    def test_create_rate_request_with_package_preset(self):
        request = gateway.mapper.create_rate_request(
            RateRequest(**RateWithPresetPayload)
        )

        # remove MessageTime, Date and ReadyTime for testing purpose
        serialized_request = re.sub(
            "<MessageTime>[^>]+</MessageTime>",
            "",
            re.sub(
                "<Date>[^>]+</Date>",
                "",
                re.sub("<ReadyTime>[^>]+</ReadyTime>", "", request.serialize()),
            ),
        )

        self.assertEqual(serialized_request, RateRequestFromPresetXML)

    @patch("purplship.mappers.dhl_express.proxy.http", return_value="<a></a>")
    def test_get_rates(self, http_mock):
        Rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, gateway.settings.server_url)

    def test_parse_rate_response(self):
        with patch("purplship.mappers.dhl_express.proxy.http") as mock:
            mock.return_value = RateResponseXML
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedRateResponse)
            )

    def test_parse_rate_parsing_error(self):
        with patch("purplship.mappers.dhl_express.proxy.http") as mock:
            mock.return_value = RateParsingError
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedRateParsingError)
            )

    def test_parse_rate_missing_args_error(self):
        with patch("purplship.mappers.dhl_express.proxy.http") as mock:
            mock.return_value = RateMissingArgsError
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedRateMissingArgsError)
            )

    def test_parse_rate_vol_weight_higher_response(self):
        with patch("purplship.mappers.dhl_express.proxy.http") as mock:
            mock.return_value = RateVolWeightHigher
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedRateVolWeightHigher)
            )


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {"postal_code": "H3N1S4", "country_code": "CA"},
    "recipient": {"city": "Lome", "country_code": "TG"},
    "parcels": [
        {
            "id": "1",
            "height": 3,
            "length": 10,
            "width": 3,
            "weight": 4.0,
            "weight_unit": "LB",
            "dimension_unit": "IN",
            "is_document": True,
        }
    ],
    "services": ["dhl_express_worldwide_doc"],
    "options": {"currency": "CAD", "insurance": 75},
}


RateWithPresetPayload = {
    "shipper": {"postal_code": "H3N1S4", "country_code": "CA"},
    "recipient": {"city": "Lome", "country_code": "TG"},
    "parcels": [
        {
            "package_preset": "dhl_express_tube",
        }
    ],
    "services": ["dhl_express_worldwide_nondoc"],
    "options": {"currency": "CAD"},
}

ParsedRateParsingError = [
    [],
    [
        {
            "carrier_name": "dhl_express",
            "carrier_id": "carrier_id",
            "code": "111",
            "message": 'Error in parsing request XML:Error: The\n                    content of element type "ServiceHeader"\n                    must match\n                    "(MessageTime,MessageReference,SiteID,Password)".\n                    at line 9, column 30',
        }
    ],
]

ParsedRateMissingArgsError = [
    [],
    [
        {
            "carrier_name": "dhl_express",
            "carrier_id": "carrier_id",
            "code": "340004",
            "message": "The location information is missing. At least one attribute post code, city name or suburb name should be provided",
        },
        {
            "carrier_name": "dhl_express",
            "carrier_id": "carrier_id",
            "code": "220001",
            "message": "Failure - request",
        },
    ],
]

ParsedRateResponse = [
    [
        {
            "base_charge": 195.32,
            "carrier_name": "dhl_express",
            "carrier_id": "carrier_id",
            "currency": "CAD",
            "discount": 0.0,
            "duties_and_taxes": 0.0,
            "transit_days": 5,
            "extra_charges": [
                {"amount": 12.7, "currency": "CAD", "name": "FUEL SURCHARGE"}
            ],
            "meta": {"service_name": "dhl_express_worldwide_doc"},
            "service": "dhl_express_worldwide_doc",
            "total_charge": 208.02,
        },
        {
            "base_charge": 213.47,
            "carrier_name": "dhl_express",
            "carrier_id": "carrier_id",
            "currency": "CAD",
            "discount": 0.0,
            "duties_and_taxes": 0.0,
            "transit_days": 5,
            "extra_charges": [],
            "meta": {"service_name": "dhl_express_easy_doc"},
            "service": "dhl_express_easy_doc",
            "total_charge": 213.47,
        },
    ],
    [],
]

ParsedRateVolWeightHigher = [[], []]


RateParsingError = """<?xml version="1.0" encoding="UTF-8"?>
<res:ErrorResponse xmlns:res='http://www.dhl.com' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:schemaLocation= 'http://www.dhl.com err-res.xsd'>
    <Response>
        <ServiceHeader>
            <MessageTime>2018-06-22T04:55:31+01:00</MessageTime>
            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID></SiteID>
            <Password></Password>
        </ServiceHeader>
        <Status>
            <ActionStatus>Error</ActionStatus>
            <Condition>
                <ConditionCode>111</ConditionCode>
                <ConditionData>Error in parsing request XML:Error: The
                    content of element type &quot;ServiceHeader&quot;
                    must match
                    &quot;(MessageTime,MessageReference,SiteID,Password)&quot;.
                    at line 9, column 30</ConditionData>
            </Condition>
        </Status>
    </Response>
</res:ErrorResponse><!-- ServiceInvocationId:20180622045531_96ab_f3e91245-69d2-422e-b943-83fbe8f8181b -->
"""

RateMissingArgsError = """<?xml version="1.0" ?>
<DCTResponse>
    <GetQuoteResponse>
        <Response>
            <ServiceHeader>
                <MessageTime>2018-06-22T04:49:29.292000+01:00</MessageTime>
                <MessageReference>1234567890123456789012345678901</MessageReference>
                <SiteID></SiteID>
            </ServiceHeader>
        </Response>
        <Note>
            <ActionStatus>Failure</ActionStatus>
            <Condition>
                <ConditionCode>340004</ConditionCode>
                <ConditionData>The location information is missing. At least one attribute post code, city name or suburb name should be provided</ConditionData>
            </Condition>
            <Condition>
                <ConditionCode>220001</ConditionCode>
                <ConditionData>Failure - request</ConditionData>
            </Condition>
        </Note>
    </GetQuoteResponse>
</DCTResponse>
"""

RateRequestXML = """<p:DCTRequest xmlns:p="http://www.dhl.com" xmlns:p1="http://www.dhl.com/datatypes" xmlns:p2="http://www.dhl.com/DCTRequestdatatypes" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com DCT-req.xsd " schemaVersion="2.0">
    <GetQuote>
        <Request>
            <ServiceHeader>
                
                <MessageReference>1234567890123456789012345678901</MessageReference>
                <SiteID>site_id</SiteID>
                <Password>password</Password>
            </ServiceHeader>
            <MetaData>
                <SoftwareName>3PV</SoftwareName>
                <SoftwareVersion>1.0</SoftwareVersion>
            </MetaData>
        </Request>
        <From>
            <CountryCode>CA</CountryCode>
            <Postalcode>H3N1S4</Postalcode>
        </From>
        <BkgDetails>
            <PaymentCountryCode>CA</PaymentCountryCode>
            
            
            <DimensionUnit>IN</DimensionUnit>
            <WeightUnit>LB</WeightUnit>
            <NumberOfPieces>1</NumberOfPieces>
            <ShipmentWeight>4</ShipmentWeight>
            <Pieces>
                <Piece>
                    <PieceID>1</PieceID>
                    <Height>3</Height>
                    <Depth>10</Depth>
                    <Width>3</Width>
                    <Weight>4</Weight>
                </Piece>
            </Pieces>
            <PaymentAccountNumber>123456789</PaymentAccountNumber>
            <IsDutiable>N</IsDutiable>
            <NetworkTypeCode>AL</NetworkTypeCode>
            <QtdShp>
                <GlobalProductCode>D</GlobalProductCode>
                <LocalProductCode>D</LocalProductCode>
                <QtdShpExChrg>
                    <SpecialServiceType>II</SpecialServiceType>
                </QtdShpExChrg>
            </QtdShp>
            <InsuredValue>75</InsuredValue>
            <InsuredCurrency>CAD</InsuredCurrency>
        </BkgDetails>
        <To>
            <CountryCode>TG</CountryCode>
            <City>Lome</City>
        </To>
    </GetQuote>
</p:DCTRequest>
"""

RateRequestFromPresetXML = """<p:DCTRequest xmlns:p="http://www.dhl.com" xmlns:p1="http://www.dhl.com/datatypes" xmlns:p2="http://www.dhl.com/DCTRequestdatatypes" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com DCT-req.xsd " schemaVersion="2.0">
    <GetQuote>
        <Request>
            <ServiceHeader>
                
                <MessageReference>1234567890123456789012345678901</MessageReference>
                <SiteID>site_id</SiteID>
                <Password>password</Password>
            </ServiceHeader>
            <MetaData>
                <SoftwareName>3PV</SoftwareName>
                <SoftwareVersion>1.0</SoftwareVersion>
            </MetaData>
        </Request>
        <From>
            <CountryCode>CA</CountryCode>
            <Postalcode>H3N1S4</Postalcode>
        </From>
        <BkgDetails>
            <PaymentCountryCode>CA</PaymentCountryCode>
            
            
            <DimensionUnit>CM</DimensionUnit>
            <WeightUnit>KG</WeightUnit>
            <NumberOfPieces>1</NumberOfPieces>
            <ShipmentWeight>5</ShipmentWeight>
            <Pieces>
                <Piece>
                    <PieceID>1</PieceID>
                    <PackageTypeCode>COY</PackageTypeCode>
                    <Height>15</Height>
                    <Depth>15</Depth>
                    <Width>96</Width>
                    <Weight>5</Weight>
                </Piece>
            </Pieces>
            <PaymentAccountNumber>123456789</PaymentAccountNumber>
            <IsDutiable>Y</IsDutiable>
            <NetworkTypeCode>AL</NetworkTypeCode>
            <QtdShp>
                <GlobalProductCode>P</GlobalProductCode>
                <LocalProductCode>P</LocalProductCode>
                <QtdShpExChrg>
                    <SpecialServiceType>WY</SpecialServiceType>
                </QtdShpExChrg>
            </QtdShp>
        </BkgDetails>
        <To>
            <CountryCode>TG</CountryCode>
            <City>Lome</City>
        </To>
        <Dutiable>
            <DeclaredCurrency>CAD</DeclaredCurrency>
            <DeclaredValue>1.</DeclaredValue>
        </Dutiable>
    </GetQuote>
</p:DCTRequest>
"""

RateResponseXML = """<?xml version="1.0" ?>
<DCTResponse>
    <GetQuoteResponse>
        <Response>
            <ServiceHeader>
                <MessageTime>2018-06-21T11:33:15.103000+01:00</MessageTime>
                <MessageReference>1234567890123456789012345678901</MessageReference>
                <SiteID>...</SiteID>
            </ServiceHeader>
        </Response>
        <BkgDetails>
            <QtdShp>
                <OriginServiceArea>
                    <FacilityCode>GTW</FacilityCode>
                    <ServiceAreaCode>YUL</ServiceAreaCode>
                </OriginServiceArea>
                <DestinationServiceArea>
                    <FacilityCode>LFW</FacilityCode>
                    <ServiceAreaCode>LFW</ServiceAreaCode>
                </DestinationServiceArea>
                <GlobalProductCode>D</GlobalProductCode>
                <LocalProductCode>D</LocalProductCode>
                <ProductShortName>EXPRESS WORLDWIDE</ProductShortName>
                <LocalProductName>EXPRESS WORLDWIDE DOC</LocalProductName>
                <NetworkTypeCode>TD</NetworkTypeCode>
                <POfferedCustAgreement>N</POfferedCustAgreement>
                <TransInd>Y</TransInd>
                <PickupDate>2018-06-21</PickupDate>
                <PickupCutoffTime>PT17H30M</PickupCutoffTime>
                <BookingTime>PT16H30M</BookingTime>
                <CurrencyCode>CAD</CurrencyCode>
                <ExchangeRate>0.662335</ExchangeRate>
                <WeightCharge>195.319999999999993</WeightCharge>
                <WeightChargeTax>0.</WeightChargeTax>
                <TotalTransitDays>5</TotalTransitDays>
                <PickupPostalLocAddDays>0</PickupPostalLocAddDays>
                <DeliveryPostalLocAddDays>0</DeliveryPostalLocAddDays>
                <DeliveryTime>PT23H59M</DeliveryTime>
                <DimensionalWeight>0.647</DimensionalWeight>
                <WeightUnit>L</WeightUnit>
                <PickupDayOfWeekNum>4</PickupDayOfWeekNum>
                <DestinationDayOfWeekNum>2</DestinationDayOfWeekNum>
                <QuotedWeight>4.</QuotedWeight>
                <QuotedWeightUOM>KG</QuotedWeightUOM>
                <QtdShpExChrg>
                    <SpecialServiceType>FF</SpecialServiceType>
                    <LocalServiceType>FF</LocalServiceType>
                    <GlobalServiceName>FUEL SURCHARGE</GlobalServiceName>
                    <LocalServiceTypeName>FUEL SURCHARGE</LocalServiceTypeName>
                    <SOfferedCustAgreement>N</SOfferedCustAgreement>
                    <ChargeCodeType>SCH</ChargeCodeType>
                    <CurrencyCode>CAD</CurrencyCode>
                    <ChargeValue>12.699999999999999</ChargeValue>
                    <QtdSExtrChrgInAdCur>
                        <ChargeValue>12.699999999999999</ChargeValue>
                        <CurrencyCode>CAD</CurrencyCode>
                        <CurrencyRoleTypeCode>BILLC</CurrencyRoleTypeCode>
                    </QtdSExtrChrgInAdCur>
                    <QtdSExtrChrgInAdCur>
                        <ChargeValue>12.699999999999999</ChargeValue>
                        <CurrencyCode>CAD</CurrencyCode>
                        <CurrencyRoleTypeCode>PULCL</CurrencyRoleTypeCode>
                    </QtdSExtrChrgInAdCur>
                    <QtdSExtrChrgInAdCur>
                        <ChargeValue>8.41</ChargeValue>
                        <CurrencyCode>EUR</CurrencyCode>
                        <CurrencyRoleTypeCode>BASEC</CurrencyRoleTypeCode>
                    </QtdSExtrChrgInAdCur>
                </QtdShpExChrg>
                <PricingDate>2018-06-21</PricingDate>
                <ShippingCharge>208.02000000000001</ShippingCharge>
                <TotalTaxAmount>0.</TotalTaxAmount>
                <PickupWindowEarliestTime>09:00:00</PickupWindowEarliestTime>
                <PickupWindowLatestTime>19:00:00</PickupWindowLatestTime>
                <BookingCutoffOffset>PT1H</BookingCutoffOffset>
                <DeliveryDate>
                    <DeliveryType>QDDC</DeliveryType>
                    <DlvyDateTime>2018-06-26 11:59:00</DlvyDateTime>
                    <DeliveryDateTimeOffset>+00:00</DeliveryDateTimeOffset>
                </DeliveryDate>
            </QtdShp>
            <QtdShp>
                <OriginServiceArea>
                    <FacilityCode>GTW</FacilityCode>
                    <ServiceAreaCode>YUL</ServiceAreaCode>
                </OriginServiceArea>
                <DestinationServiceArea>
                    <FacilityCode>LFW</FacilityCode>
                    <ServiceAreaCode>LFW</ServiceAreaCode>
                </DestinationServiceArea>
                <GlobalProductCode>7</GlobalProductCode>
                <LocalProductCode>7</LocalProductCode>
                <ProductShortName>EXPRESS EASY</ProductShortName>
                <LocalProductName>EXPRESS EASY DOC</LocalProductName>
                <NetworkTypeCode>TD</NetworkTypeCode>
                <POfferedCustAgreement>Y</POfferedCustAgreement>
                <TransInd>N</TransInd>
                <PickupDate>2018-06-21</PickupDate>
                <PickupCutoffTime>PT17H30M</PickupCutoffTime>
                <BookingTime>PT16H30M</BookingTime>
                <CurrencyCode>CAD</CurrencyCode>
                <ExchangeRate>0.662335</ExchangeRate>
                <WeightCharge>213.469999999999999</WeightCharge>
                <WeightChargeTax>0.</WeightChargeTax>
                <TotalTransitDays>5</TotalTransitDays>
                <PickupPostalLocAddDays>0</PickupPostalLocAddDays>
                <DeliveryPostalLocAddDays>0</DeliveryPostalLocAddDays>
                <DeliveryTime>PT23H59M</DeliveryTime>
                <DimensionalWeight>0.647</DimensionalWeight>
                <WeightUnit>LB</WeightUnit>
                <PickupDayOfWeekNum>4</PickupDayOfWeekNum>
                <DestinationDayOfWeekNum>2</DestinationDayOfWeekNum>
                <QuotedWeight>4.</QuotedWeight>
                <QuotedWeightUOM>KG</QuotedWeightUOM>
                <PricingDate>2018-06-21</PricingDate>
                <ShippingCharge>213.469999999999999</ShippingCharge>
                <TotalTaxAmount>0.</TotalTaxAmount>
                <PickupWindowEarliestTime>09:00:00</PickupWindowEarliestTime>
                <PickupWindowLatestTime>19:00:00</PickupWindowLatestTime>
                <BookingCutoffOffset>PT1H</BookingCutoffOffset>
                <DeliveryDate>
                    <DeliveryType>QDDC</DeliveryType>
                    <DlvyDateTime>2018-06-26 11:59:00</DlvyDateTime>
                    <DeliveryDateTimeOffset>+00:00</DeliveryDateTimeOffset>
                </DeliveryDate>
            </QtdShp>
        </BkgDetails>
        <Srvs>
            <Srv>
                <GlobalProductCode>D</GlobalProductCode>
                <MrkSrv>
                    <LocalProductCode>D</LocalProductCode>
                    <ProductShortName>EXPRESS WORLDWIDE</ProductShortName>
                    <LocalProductName>EXPRESS WORLDWIDE DOC</LocalProductName>
                    <ProductDesc>EXPRESS WORLDWIDE DOC</ProductDesc>
                    <NetworkTypeCode>TD</NetworkTypeCode>
                    <POfferedCustAgreement>N</POfferedCustAgreement>
                    <TransInd>Y</TransInd>
                    <LocalProductCtryCd>CA</LocalProductCtryCd>
                    <GlobalServiceType>D</GlobalServiceType>
                    <LocalServiceName>EXPRESS WORLDWIDE DOC</LocalServiceName>
                </MrkSrv>
                <MrkSrv>
                    <LocalServiceType>FF</LocalServiceType>
                    <GlobalServiceName>FUEL SURCHARGE</GlobalServiceName>
                    <LocalServiceTypeName>FUEL SURCHARGE</LocalServiceTypeName>
                    <SOfferedCustAgreement>N</SOfferedCustAgreement>
                    <ChargeCodeType>SCH</ChargeCodeType>
                    <MrkSrvInd>N</MrkSrvInd>
                    <GlobalServiceType>FF</GlobalServiceType>
                    <LocalServiceName>FUEL SURCHARGE</LocalServiceName>
                </MrkSrv>
            </Srv>
            <Srv>
                <GlobalProductCode>7</GlobalProductCode>
                <MrkSrv>
                    <LocalProductCode>7</LocalProductCode>
                    <ProductShortName>EXPRESS EASY</ProductShortName>
                    <LocalProductName>EXPRESS EASY DOC</LocalProductName>
                    <ProductDesc>EXPRESS EASY DOC</ProductDesc>
                    <NetworkTypeCode>TD</NetworkTypeCode>
                    <POfferedCustAgreement>Y</POfferedCustAgreement>
                    <TransInd>N</TransInd>
                    <LocalProductCtryCd>CA</LocalProductCtryCd>
                    <GlobalServiceType>7</GlobalServiceType>
                    <LocalServiceName>EXPRESS EASY DOC</LocalServiceName>
                </MrkSrv>
            </Srv>
        </Srvs>
        <Note>
            <ActionStatus>Success</ActionStatus>
        </Note>
    </GetQuoteResponse>
</DCTResponse>
"""

RateVolWeightHigher = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<res:DCTResponse xmlns:res='http://www.dhl.com' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:schemaLocation= 'http://www.dhl.com DCT-Response.xsd'>
    <GetQuoteResponse>
        <Response>
            <ServiceHeader>
                <MessageTime>2017-11-08T10:43:44.037+01:00</MessageTime>
                <MessageReference>1234567890123456789012345678901</MessageReference>
                <SiteID>xmlpidev</SiteID>
            </ServiceHeader>
        </Response>
        <BkgDetails>
            <QtdShp>
                <OriginServiceArea>
                    <FacilityCode>NIC</FacilityCode>
                    <ServiceAreaCode>LCA</ServiceAreaCode>
                </OriginServiceArea>
                <DestinationServiceArea>
                    <FacilityCode>AEC</FacilityCode>
                    <ServiceAreaCode>ATH</ServiceAreaCode>
                </DestinationServiceArea>
                <GlobalProductCode>P</GlobalProductCode>
                <LocalProductCode>P</LocalProductCode>
                <ProductShortName>EXPRESS WORLDWIDE</ProductShortName>
                <LocalProductName>EXPRESS WORLDWIDE NONDOC</LocalProductName>
                <NetworkTypeCode>TD</NetworkTypeCode>
                <POfferedCustAgreement>N</POfferedCustAgreement>
                <TransInd>Y</TransInd>
                <PickupDate>2017-11-10</PickupDate>
                <PickupCutoffTime>PT13H30M</PickupCutoffTime>
                <BookingTime>PT12H30M</BookingTime>
                <ExchangeRate>0.000</ExchangeRate>
                <WeightCharge>0</WeightCharge>
                <WeightChargeTax>0.000</WeightChargeTax>
                <TotalTransitDays>1</TotalTransitDays>
                <PickupPostalLocAddDays>0</PickupPostalLocAddDays>
                <DeliveryPostalLocAddDays>0</DeliveryPostalLocAddDays>
                <PickupNonDHLCourierCode> </PickupNonDHLCourierCode>
                <DeliveryNonDHLCourierCode> </DeliveryNonDHLCourierCode>
                <DeliveryDate>
                    <DeliveryType>QDDC</DeliveryType>
                    <DlvyDateTime>2017-11-13 11:59:00</DlvyDateTime>
                    <DeliveryDateTimeOffset>+00:00</DeliveryDateTimeOffset>
                </DeliveryDate>
                <DeliveryTime>PT23H59M</DeliveryTime>
                <DimensionalWeight>70.000</DimensionalWeight>
                <WeightUnit>KG</WeightUnit>
                <PickupDayOfWeekNum>5</PickupDayOfWeekNum>
                <DestinationDayOfWeekNum>1</DestinationDayOfWeekNum>
                <PricingDate>2017-11-08</PricingDate>
                <TotalTaxAmount>0.000</TotalTaxAmount>
                <PickupWindowEarliestTime>09:00:00</PickupWindowEarliestTime>
                <PickupWindowLatestTime>17:00:00</PickupWindowLatestTime>
                <BookingCutoffOffset>PT1H</BookingCutoffOffset>
            </QtdShp>
        </BkgDetails>
        <Srvs>
            <Srv>
                <GlobalProductCode>P</GlobalProductCode>
                <MrkSrv>
                    <LocalProductCode>P</LocalProductCode>
                    <ProductShortName>EXPRESS WORLDWIDE</ProductShortName>
                    <LocalProductName>EXPRESS WORLDWIDE NONDOC</LocalProductName>
                    <ProductDesc>EXPRESS WORLDWIDE NONDOC</ProductDesc>
                    <NetworkTypeCode>TD</NetworkTypeCode>
                    <POfferedCustAgreement>N</POfferedCustAgreement>
                    <TransInd>Y</TransInd>
                    <LocalProductCtryCd>CY</LocalProductCtryCd>
                    <GlobalServiceType>P</GlobalServiceType>
                    <LocalServiceName>EXPRESS WORLDWIDE NONDOC</LocalServiceName>
                </MrkSrv>
            </Srv>
        </Srvs>
        <Note>
            <ActionStatus>Success</ActionStatus>
        </Note>
    </GetQuoteResponse>
</res:DCTResponse>
"""
