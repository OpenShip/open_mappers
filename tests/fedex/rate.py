import re
import unittest
import logging
from unittest.mock import patch
from purplship.core.utils import DP
from purplship.core.models import RateRequest
from purplship import Rating
from tests.fedex.fixture import gateway

logger = logging.getLogger(__name__)


class TestFeDexQuote(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RateRequestPayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        # Remove timeStamp for testing
        serialized_request = re.sub(
            "<v28:ShipTimestamp>[^>]+</v28:ShipTimestamp>", "", request.serialize()
        )
        self.assertEqual(serialized_request, RateRequestXml)

    def test_create_rate_request_with_preset_package(self):
        request = gateway.mapper.create_rate_request(
            RateRequest(**RateWithPresetPayload)
        )
        # Remove timeStamp for testing
        serialized_request = re.sub(
            "<v28:ShipTimestamp>[^>]+</v28:ShipTimestamp>", "", request.serialize()
        )

        self.assertEqual(serialized_request, RateRequestUsingPackagePresetXML)

    @patch("purplship.mappers.fedex.proxy.http", return_value="<a></a>")
    def test_get_rates(self, http_mock):
        Rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{gateway.settings.server_url}/rate")

    def test_parse_rate_response(self):
        with patch("purplship.mappers.fedex.proxy.http") as mock:
            mock.return_value = RateResponseXml
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedRateResponse)
            )

    def test_parse_rate_error_response(self):
        with patch("purplship.mappers.fedex.proxy.http") as mock:
            mock.return_value = RateErrorResponseXml
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedRateErrorResponse)
            )


if __name__ == "__main__":
    unittest.main()

RateRequestPayload = {
    "shipper": {"postal_code": "H3N1S4", "country_code": "CA"},
    "recipient": {"city": "Lome", "country_code": "TG"},
    "parcels": [{"id": "1", "height": 3, "length": 10, "width": 3, "weight": 4.0}],
    "options": {"currency": "USD"},
}

RateWithPresetPayload = {
    "shipper": {"postal_code": "H3N1S4", "country_code": "CA"},
    "recipient": {"city": "Lome", "country_code": "TG"},
    "parcels": [{"id": "1", "package_preset": "fedex_pak"}],
    "options": {"currency": "USD"},
}

ParsedRateResponse = [
    [
        {
            "base_charge": 245.35,
            "carrier_id": "carrier_id",
            "carrier_name": "fedex",
            "currency": "CAD",
            "discount": 50.66,
            "duties_and_taxes": 13.53,
            "extra_charges": [
                {"amount": 25.31, "currency": "CAD", "name": "Fuel"},
                {
                    "amount": 13.53,
                    "currency": "CAD",
                    "name": "Canada freight goods and services",
                },
            ],
            "meta": {"service_name": "fedex_first_overnight"},
            "service": "fedex_first_overnight",
            "total_charge": 284.19,
        },
        {
            "base_charge": 229.15,
            "carrier_id": "carrier_id",
            "carrier_name": "fedex",
            "currency": "CAD",
            "discount": 45.96,
            "duties_and_taxes": 12.64,
            "extra_charges": [
                {"amount": 23.63, "currency": "CAD", "name": "Fuel"},
                {
                    "amount": 12.64,
                    "currency": "CAD",
                    "name": "Canada freight goods and services",
                },
            ],
            "meta": {"service_name": "fedex_priority_overnight"},
            "service": "fedex_priority_overnight",
            "total_charge": 265.42,
        },
        {
            "base_charge": 208.55,
            "carrier_id": "carrier_id",
            "carrier_name": "fedex",
            "currency": "CAD",
            "discount": 41.63,
            "duties_and_taxes": 11.5,
            "extra_charges": [
                {"amount": 21.51, "currency": "CAD", "name": "Fuel"},
                {
                    "amount": 11.5,
                    "currency": "CAD",
                    "name": "Canada freight goods and services",
                },
            ],
            "meta": {"service_name": "fedex_standard_overnight"},
            "service": "fedex_standard_overnight",
            "total_charge": 241.56,
        },
        {
            "base_charge": 195.2,
            "carrier_id": "carrier_id",
            "carrier_name": "fedex",
            "currency": "CAD",
            "discount": 141.04,
            "duties_and_taxes": 5.92,
            "extra_charges": [
                {"amount": 11.07, "currency": "CAD", "name": "Fuel"},
                {
                    "amount": 5.92,
                    "currency": "CAD",
                    "name": "Canada freight goods and services",
                },
            ],
            "meta": {"service_name": "fedex_2_day"},
            "service": "fedex_2_day",
            "total_charge": 124.35,
        },
        {
            "base_charge": 124.7,
            "carrier_id": "carrier_id",
            "carrier_name": "fedex",
            "currency": "CAD",
            "discount": 138.42,
            "duties_and_taxes": 1.51,
            "extra_charges": [
                {"amount": 2.83, "currency": "CAD", "name": "Fuel"},
                {
                    "amount": 1.51,
                    "currency": "CAD",
                    "name": "Canada freight goods and services",
                },
            ],
            "meta": {"service_name": "fedex_express_saver"},
            "service": "fedex_express_saver",
            "total_charge": 31.77,
        },
        {
            "base_charge": 27.99,
            "carrier_id": "carrier_id",
            "carrier_name": "fedex",
            "currency": "CAD",
            "discount": 47.25,
            "duties_and_taxes": 1.59,
            "extra_charges": [
                {"amount": 3.85, "currency": "CAD", "name": "FedEx Ground Fuel"},
                {
                    "amount": 1.59,
                    "currency": "CAD",
                    "name": "Canada goods and services",
                },
            ],
            "meta": {"service_name": "fedex_ground"},
            "service": "fedex_ground",
            "total_charge": 33.43,
        },
    ],
    [],
]

ParsedRateErrorResponse = [
    [],
    [
        {
            "carrier_name": "fedex",
            "carrier_id": "carrier_id",
            "code": "873",
            "message": "All specified account numbers must match.  ",
        }
    ],
]

RateErrorResponseXml = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header/>
    <SOAP-ENV:Body>
        <RateReply xmlns="http://fedex.com/ws/rate/v22">
            <HighestSeverity>ERROR</HighestSeverity>
            <Notifications>
                <Severity>ERROR</Severity>
                <Source>crs</Source>
                <Code>873</Code>
                <Message>All specified account numbers must match.  </Message>
                <LocalizedMessage>All specified account numbers must match.  </LocalizedMessage>
            </Notifications>
            <TransactionDetail>
                <CustomerTransactionId>TC023_US_PRIORITY_OVERNIGHT with Your Packaging</CustomerTransactionId>
            </TransactionDetail>
            <Version>
                <ServiceId>crs</ServiceId>
                <Major>22</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
        </RateReply>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

RateRequestXml = f"""<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:v28="http://fedex.com/ws/rate/v28">
    <tns:Body>
        <v28:RateRequest>
            <v28:WebAuthenticationDetail>
                <v28:UserCredential>
                    <v28:Key>user_key</v28:Key>
                    <v28:Password>password</v28:Password>
                </v28:UserCredential>
            </v28:WebAuthenticationDetail>
            <v28:ClientDetail>
                <v28:AccountNumber>2349857</v28:AccountNumber>
                <v28:MeterNumber>1293587</v28:MeterNumber>
            </v28:ClientDetail>
            <v28:TransactionDetail>
                <v28:CustomerTransactionId>FTC</v28:CustomerTransactionId>
            </v28:TransactionDetail>
            <v28:Version>
                <v28:ServiceId>crs</v28:ServiceId>
                <v28:Major>28</v28:Major>
                <v28:Intermediate>0</v28:Intermediate>
                <v28:Minor>0</v28:Minor>
            </v28:Version>
            <v28:ReturnTransitAndCommit>true</v28:ReturnTransitAndCommit>
            <v28:RequestedShipment>
                
                <v28:DropoffType>REGULAR_PICKUP</v28:DropoffType>
                <v28:PackagingType>YOUR_PACKAGING</v28:PackagingType>
                <v28:TotalWeight>
                    <v28:Units>LB</v28:Units>
                    <v28:Value>4</v28:Value>
                </v28:TotalWeight>
                <v28:PreferredCurrency>USD</v28:PreferredCurrency>
                <v28:Shipper>
                    <v28:AccountNumber>2349857</v28:AccountNumber>
                    <v28:Address>
                        <v28:PostalCode>H3N1S4</v28:PostalCode>
                        <v28:CountryCode>CA</v28:CountryCode>
                        <v28:CountryName>Canada</v28:CountryName>
                        <v28:Residential>false</v28:Residential>
                    </v28:Address>
                </v28:Shipper>
                <v28:Recipient>
                    <v28:Address>
                        <v28:City>Lome</v28:City>
                        <v28:CountryCode>TG</v28:CountryCode>
                        <v28:CountryName>Togo</v28:CountryName>
                        <v28:Residential>false</v28:Residential>
                    </v28:Address>
                </v28:Recipient>
                <v28:RateRequestTypes>LIST</v28:RateRequestTypes>
                <v28:RateRequestTypes>PREFERRED</v28:RateRequestTypes>
                <v28:PackageCount>1</v28:PackageCount>
                <v28:RequestedPackageLineItems>
                    <v28:SequenceNumber>1</v28:SequenceNumber>
                    <v28:GroupPackageCount>1</v28:GroupPackageCount>
                    <v28:Weight>
                        <v28:Units>LB</v28:Units>
                        <v28:Value>4</v28:Value>
                    </v28:Weight>
                    <v28:Dimensions>
                        <v28:Length>10</v28:Length>
                        <v28:Width>3</v28:Width>
                        <v28:Height>3</v28:Height>
                        <v28:Units>IN</v28:Units>
                    </v28:Dimensions>
                </v28:RequestedPackageLineItems>
            </v28:RequestedShipment>
        </v28:RateRequest>
    </tns:Body>
</tns:Envelope>
"""

RateRequestUsingPackagePresetXML = f"""<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:v28="http://fedex.com/ws/rate/v28">
    <tns:Body>
        <v28:RateRequest>
            <v28:WebAuthenticationDetail>
                <v28:UserCredential>
                    <v28:Key>user_key</v28:Key>
                    <v28:Password>password</v28:Password>
                </v28:UserCredential>
            </v28:WebAuthenticationDetail>
            <v28:ClientDetail>
                <v28:AccountNumber>2349857</v28:AccountNumber>
                <v28:MeterNumber>1293587</v28:MeterNumber>
            </v28:ClientDetail>
            <v28:TransactionDetail>
                <v28:CustomerTransactionId>FTC</v28:CustomerTransactionId>
            </v28:TransactionDetail>
            <v28:Version>
                <v28:ServiceId>crs</v28:ServiceId>
                <v28:Major>28</v28:Major>
                <v28:Intermediate>0</v28:Intermediate>
                <v28:Minor>0</v28:Minor>
            </v28:Version>
            <v28:ReturnTransitAndCommit>true</v28:ReturnTransitAndCommit>
            <v28:RequestedShipment>
                
                <v28:DropoffType>REGULAR_PICKUP</v28:DropoffType>
                <v28:PackagingType>FEDEX_PAK</v28:PackagingType>
                <v28:TotalWeight>
                    <v28:Units>LB</v28:Units>
                    <v28:Value>2.2</v28:Value>
                </v28:TotalWeight>
                <v28:PreferredCurrency>USD</v28:PreferredCurrency>
                <v28:Shipper>
                    <v28:AccountNumber>2349857</v28:AccountNumber>
                    <v28:Address>
                        <v28:PostalCode>H3N1S4</v28:PostalCode>
                        <v28:CountryCode>CA</v28:CountryCode>
                        <v28:CountryName>Canada</v28:CountryName>
                        <v28:Residential>false</v28:Residential>
                    </v28:Address>
                </v28:Shipper>
                <v28:Recipient>
                    <v28:Address>
                        <v28:City>Lome</v28:City>
                        <v28:CountryCode>TG</v28:CountryCode>
                        <v28:CountryName>Togo</v28:CountryName>
                        <v28:Residential>false</v28:Residential>
                    </v28:Address>
                </v28:Recipient>
                <v28:RateRequestTypes>LIST</v28:RateRequestTypes>
                <v28:RateRequestTypes>PREFERRED</v28:RateRequestTypes>
                <v28:PackageCount>1</v28:PackageCount>
                <v28:RequestedPackageLineItems>
                    <v28:SequenceNumber>1</v28:SequenceNumber>
                    <v28:GroupPackageCount>1</v28:GroupPackageCount>
                    <v28:Weight>
                        <v28:Units>LB</v28:Units>
                        <v28:Value>2.2</v28:Value>
                    </v28:Weight>
                    <v28:Dimensions>
                        <v28:Length>1</v28:Length>
                        <v28:Width>11</v28:Width>
                        <v28:Height>14</v28:Height>
                        <v28:Units>IN</v28:Units>
                    </v28:Dimensions>
                </v28:RequestedPackageLineItems>
            </v28:RequestedShipment>
        </v28:RateRequest>
    </tns:Body>
</tns:Envelope>
"""

RateResponseXml = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header/>
    <SOAP-ENV:Body>
        <RateReply xmlns="http://fedex.com/ws/rate/v28">
            <HighestSeverity>NOTE</HighestSeverity>
            <Notifications>
                <Severity>NOTE</Severity>
                <Source>crs</Source>
                <Code>819</Code>
                <Message>The origin state/province code has been changed.  </Message>
                <LocalizedMessage>The origin state/province code has been changed.  </LocalizedMessage>
            </Notifications>
            <TransactionDetail>
                <CustomerTransactionId>FTC</CustomerTransactionId>
            </TransactionDetail>
            <Version>
                <ServiceId>crs</ServiceId>
                <Major>28</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
            <RateReplyDetails>
                <ServiceType>FIRST_OVERNIGHT</ServiceType>
                <ServiceDescription>
                    <ServiceType>FIRST_OVERNIGHT</ServiceType>
                    <Code>06</Code>
                    <Names>
                        <Type>long</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FedEx First OvernightÂ®</Value>
                    </Names>
                    <Names>
                        <Type>long</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FedEx First Overnight</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FedEx First OvernightÂ®</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FedEx First Overnight</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FO</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FO</Value>
                    </Names>
                    <Names>
                        <Type>abbrv</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FO</Value>
                    </Names>
                    <Description>First Overnight</Description>
                    <AstraDescription>1ST OVR</AstraDescription>
                </ServiceDescription>
                <PackagingType>YOUR_PACKAGING</PackagingType>
                <DeliveryStation>YVRA </DeliveryStation>
                <DeliveryDayOfWeek>FRI</DeliveryDayOfWeek>
                <CommitDetails>
                    <ServiceType>FIRST_OVERNIGHT</ServiceType>
                    <ServiceDescription>
                        <ServiceType>FIRST_OVERNIGHT</ServiceType>
                        <Code>06</Code>
                        <Names>
                            <Type>long</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>FedEx First OvernightÂ®</Value>
                        </Names>
                        <Names>
                            <Type>long</Type>
                            <Encoding>ascii</Encoding>
                            <Value>FedEx First Overnight</Value>
                        </Names>
                        <Names>
                            <Type>medium</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>FedEx First OvernightÂ®</Value>
                        </Names>
                        <Names>
                            <Type>medium</Type>
                            <Encoding>ascii</Encoding>
                            <Value>FedEx First Overnight</Value>
                        </Names>
                        <Names>
                            <Type>short</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>FO</Value>
                        </Names>
                        <Names>
                            <Type>short</Type>
                            <Encoding>ascii</Encoding>
                            <Value>FO</Value>
                        </Names>
                        <Names>
                            <Type>abbrv</Type>
                            <Encoding>ascii</Encoding>
                            <Value>FO</Value>
                        </Names>
                        <Description>First Overnight</Description>
                        <AstraDescription>1ST OVR</AstraDescription>
                    </ServiceDescription>
                    <DerivedShipmentSignatureOption>
                        <OptionType>SERVICE_DEFAULT</OptionType>
                    </DerivedShipmentSignatureOption>
                    <DerivedOriginDetail>
                        <CountryCode>CA</CountryCode>
                        <StateOrProvinceCode>PQ</StateOrProvinceCode>
                        <PostalCode>J7H1H5</PostalCode>
                        <ServiceArea>A2</ServiceArea>
                        <LocationId>YMXA </LocationId>
                        <LocationNumber>0</LocationNumber>
                    </DerivedOriginDetail>
                    <DerivedDestinationDetail>
                        <CountryCode>CA</CountryCode>
                        <StateOrProvinceCode>BC</StateOrProvinceCode>
                        <PostalCode>V6M2V9</PostalCode>
                        <ServiceArea>A2</ServiceArea>
                        <LocationId>YVRA </LocationId>
                        <LocationNumber>0</LocationNumber>
                        <AirportId>YVR</AirportId>
                    </DerivedDestinationDetail>
                    <CommitTimestamp>2021-06-18T10:00:00</CommitTimestamp>
                    <DayOfWeek>FRI</DayOfWeek>
                    <DestinationServiceArea>A2</DestinationServiceArea>
                    <BrokerToDestinationDays>0</BrokerToDestinationDays>
                    <DocumentContent>NON_DOCUMENTS</DocumentContent>
                </CommitDetails>
                <DestinationAirportId>YVR</DestinationAirportId>
                <IneligibleForMoneyBackGuarantee>false</IneligibleForMoneyBackGuarantee>
                <OriginServiceArea>A2</OriginServiceArea>
                <DestinationServiceArea>A2</DestinationServiceArea>
                <SignatureOption>SERVICE_DEFAULT</SignatureOption>
                <ActualRateType>PAYOR_ACCOUNT_SHIPMENT</ActualRateType>
                <RatedShipmentDetails>
                    <EffectiveNetDiscount>
                        <Currency>CAD</Currency>
                        <Amount>50.66</Amount>
                    </EffectiveNetDiscount>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_ACCOUNT_SHIPMENT</RateType>
                        <RateScale>0000000</RateScale>
                        <RateZone>R0025</RateZone>
                        <PricingCode>ACTUAL</PricingCode>
                        <RatedWeightMethod>DIM</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>CAD</FromCurrency>
                            <IntoCurrency>CAD</IntoCurrency>
                            <Rate>1.0</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>166</DimDivisor>
                        <DimDivisorType>CUSTOMER</DimDivisorType>
                        <FuelSurchargePercent>13.75</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>KG</Units>
                            <Value>14.4</Value>
                        </TotalBillingWeight>
                        <TotalDimWeight>
                            <Units>KG</Units>
                            <Value>14.4</Value>
                        </TotalDimWeight>
                        <TotalBaseCharge>
                            <Currency>CAD</Currency>
                            <Amount>245.35</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>CAD</Currency>
                            <Amount>245.35</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>CAD</Currency>
                            <Amount>25.31</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>CAD</Currency>
                            <Amount>270.66</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>CAD</Currency>
                            <Amount>13.53</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>CAD</Currency>
                            <Amount>284.19</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>284.19</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>25.31</Amount>
                            </Amount>
                        </Surcharges>
                        <Taxes>
                            <TaxType>GST</TaxType>
                            <Description>Canada freight goods and services</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>13.53</Amount>
                            </Amount>
                        </Taxes>
                    </ShipmentRateDetail>
                </RatedShipmentDetails>
                <RatedShipmentDetails>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_LIST_SHIPMENT</RateType>
                        <RateScale>0000000</RateScale>
                        <RateZone>R0025</RateZone>
                        <PricingCode>ACTUAL</PricingCode>
                        <RatedWeightMethod>DIM</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>CAD</FromCurrency>
                            <IntoCurrency>CAD</IntoCurrency>
                            <Rate>1.0</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>139</DimDivisor>
                        <DimDivisorType>COUNTRY</DimDivisorType>
                        <FuelSurchargePercent>13.75</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>KG</Units>
                            <Value>17.1</Value>
                        </TotalBillingWeight>
                        <TotalDimWeight>
                            <Units>KG</Units>
                            <Value>17.1</Value>
                        </TotalDimWeight>
                        <TotalBaseCharge>
                            <Currency>CAD</Currency>
                            <Amount>280.35</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>CAD</Currency>
                            <Amount>280.35</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>CAD</Currency>
                            <Amount>38.55</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>CAD</Currency>
                            <Amount>318.9</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>CAD</Currency>
                            <Amount>15.95</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>CAD</Currency>
                            <Amount>334.85</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>334.85</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>38.55</Amount>
                            </Amount>
                        </Surcharges>
                        <Taxes>
                            <TaxType>GST</TaxType>
                            <Description>Canada freight goods and services</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>15.95</Amount>
                            </Amount>
                        </Taxes>
                    </ShipmentRateDetail>
                </RatedShipmentDetails>
            </RateReplyDetails>
            <RateReplyDetails>
                <ServiceType>PRIORITY_OVERNIGHT</ServiceType>
                <ServiceDescription>
                    <ServiceType>PRIORITY_OVERNIGHT</ServiceType>
                    <Code>01</Code>
                    <Names>
                        <Type>long</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FedEx Priority OvernightÂ®</Value>
                    </Names>
                    <Names>
                        <Type>long</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FedEx Priority Overnight</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FedEx Priority OvernightÂ®</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FedEx Priority Overnight</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>P-1</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>ascii</Encoding>
                        <Value>P-1</Value>
                    </Names>
                    <Names>
                        <Type>abbrv</Type>
                        <Encoding>ascii</Encoding>
                        <Value>PO</Value>
                    </Names>
                    <Description>Priority Overnight</Description>
                    <AstraDescription>PO</AstraDescription>
                </ServiceDescription>
                <PackagingType>YOUR_PACKAGING</PackagingType>
                <DeliveryStation>YVRA </DeliveryStation>
                <DeliveryDayOfWeek>FRI</DeliveryDayOfWeek>
                <CommitDetails>
                    <ServiceType>PRIORITY_OVERNIGHT</ServiceType>
                    <ServiceDescription>
                        <ServiceType>PRIORITY_OVERNIGHT</ServiceType>
                        <Code>01</Code>
                        <Names>
                            <Type>long</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>FedEx Priority OvernightÂ®</Value>
                        </Names>
                        <Names>
                            <Type>long</Type>
                            <Encoding>ascii</Encoding>
                            <Value>FedEx Priority Overnight</Value>
                        </Names>
                        <Names>
                            <Type>medium</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>FedEx Priority OvernightÂ®</Value>
                        </Names>
                        <Names>
                            <Type>medium</Type>
                            <Encoding>ascii</Encoding>
                            <Value>FedEx Priority Overnight</Value>
                        </Names>
                        <Names>
                            <Type>short</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>P-1</Value>
                        </Names>
                        <Names>
                            <Type>short</Type>
                            <Encoding>ascii</Encoding>
                            <Value>P-1</Value>
                        </Names>
                        <Names>
                            <Type>abbrv</Type>
                            <Encoding>ascii</Encoding>
                            <Value>PO</Value>
                        </Names>
                        <Description>Priority Overnight</Description>
                        <AstraDescription>PO</AstraDescription>
                    </ServiceDescription>
                    <DerivedShipmentSignatureOption>
                        <OptionType>SERVICE_DEFAULT</OptionType>
                    </DerivedShipmentSignatureOption>
                    <DerivedOriginDetail>
                        <CountryCode>CA</CountryCode>
                        <StateOrProvinceCode>PQ</StateOrProvinceCode>
                        <PostalCode>J7H1H5</PostalCode>
                        <ServiceArea>A2</ServiceArea>
                        <LocationId>YMXA </LocationId>
                        <LocationNumber>0</LocationNumber>
                    </DerivedOriginDetail>
                    <DerivedDestinationDetail>
                        <CountryCode>CA</CountryCode>
                        <StateOrProvinceCode>BC</StateOrProvinceCode>
                        <PostalCode>V6M2V9</PostalCode>
                        <ServiceArea>A2</ServiceArea>
                        <LocationId>YVRA </LocationId>
                        <LocationNumber>0</LocationNumber>
                        <AirportId>YVR</AirportId>
                    </DerivedDestinationDetail>
                    <CommitTimestamp>2021-06-18T12:00:00</CommitTimestamp>
                    <DayOfWeek>FRI</DayOfWeek>
                    <DestinationServiceArea>A2</DestinationServiceArea>
                    <BrokerToDestinationDays>0</BrokerToDestinationDays>
                    <DocumentContent>NON_DOCUMENTS</DocumentContent>
                </CommitDetails>
                <DestinationAirportId>YVR</DestinationAirportId>
                <IneligibleForMoneyBackGuarantee>false</IneligibleForMoneyBackGuarantee>
                <OriginServiceArea>A2</OriginServiceArea>
                <DestinationServiceArea>A2</DestinationServiceArea>
                <SignatureOption>SERVICE_DEFAULT</SignatureOption>
                <ActualRateType>PAYOR_ACCOUNT_SHIPMENT</ActualRateType>
                <RatedShipmentDetails>
                    <EffectiveNetDiscount>
                        <Currency>CAD</Currency>
                        <Amount>45.96</Amount>
                    </EffectiveNetDiscount>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_ACCOUNT_SHIPMENT</RateType>
                        <RateScale>0000000</RateScale>
                        <RateZone>R0025</RateZone>
                        <PricingCode>ACTUAL</PricingCode>
                        <RatedWeightMethod>DIM</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>CAD</FromCurrency>
                            <IntoCurrency>CAD</IntoCurrency>
                            <Rate>1.0</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>166</DimDivisor>
                        <DimDivisorType>PRODUCT</DimDivisorType>
                        <FuelSurchargePercent>13.75</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>KG</Units>
                            <Value>14.4</Value>
                        </TotalBillingWeight>
                        <TotalDimWeight>
                            <Units>KG</Units>
                            <Value>14.4</Value>
                        </TotalDimWeight>
                        <TotalBaseCharge>
                            <Currency>CAD</Currency>
                            <Amount>229.15</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>CAD</Currency>
                            <Amount>229.15</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>CAD</Currency>
                            <Amount>23.63</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>CAD</Currency>
                            <Amount>252.78</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>CAD</Currency>
                            <Amount>12.64</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>CAD</Currency>
                            <Amount>265.42</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>265.42</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>23.63</Amount>
                            </Amount>
                        </Surcharges>
                        <Taxes>
                            <TaxType>GST</TaxType>
                            <Description>Canada freight goods and services</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>12.64</Amount>
                            </Amount>
                        </Taxes>
                    </ShipmentRateDetail>
                </RatedShipmentDetails>
                <RatedShipmentDetails>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_LIST_SHIPMENT</RateType>
                        <RateScale>0000000</RateScale>
                        <RateZone>R0025</RateZone>
                        <PricingCode>ACTUAL</PricingCode>
                        <RatedWeightMethod>DIM</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>CAD</FromCurrency>
                            <IntoCurrency>CAD</IntoCurrency>
                            <Rate>1.0</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>139</DimDivisor>
                        <DimDivisorType>COUNTRY</DimDivisorType>
                        <FuelSurchargePercent>13.75</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>KG</Units>
                            <Value>17.1</Value>
                        </TotalBillingWeight>
                        <TotalDimWeight>
                            <Units>KG</Units>
                            <Value>17.1</Value>
                        </TotalDimWeight>
                        <TotalBaseCharge>
                            <Currency>CAD</Currency>
                            <Amount>260.7</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>CAD</Currency>
                            <Amount>260.7</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>CAD</Currency>
                            <Amount>35.85</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>CAD</Currency>
                            <Amount>296.55</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>CAD</Currency>
                            <Amount>14.83</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>CAD</Currency>
                            <Amount>311.38</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>311.38</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>35.85</Amount>
                            </Amount>
                        </Surcharges>
                        <Taxes>
                            <TaxType>GST</TaxType>
                            <Description>Canada freight goods and services</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>14.83</Amount>
                            </Amount>
                        </Taxes>
                    </ShipmentRateDetail>
                </RatedShipmentDetails>
            </RateReplyDetails>
            <RateReplyDetails>
                <ServiceType>STANDARD_OVERNIGHT</ServiceType>
                <ServiceDescription>
                    <ServiceType>STANDARD_OVERNIGHT</ServiceType>
                    <Code>05</Code>
                    <Names>
                        <Type>long</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FedEx Standard OvernightÂ®</Value>
                    </Names>
                    <Names>
                        <Type>long</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FedEx Standard Overnight</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FedEx Standard OvernightÂ®</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FedEx Standard Overnight</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>SOS</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>ascii</Encoding>
                        <Value>SOS</Value>
                    </Names>
                    <Names>
                        <Type>abbrv</Type>
                        <Encoding>ascii</Encoding>
                        <Value>SO</Value>
                    </Names>
                    <Description>Standard Overnight</Description>
                    <AstraDescription>STD OVR</AstraDescription>
                </ServiceDescription>
                <PackagingType>YOUR_PACKAGING</PackagingType>
                <DeliveryStation>YVRA </DeliveryStation>
                <DeliveryDayOfWeek>FRI</DeliveryDayOfWeek>
                <CommitDetails>
                    <ServiceType>STANDARD_OVERNIGHT</ServiceType>
                    <ServiceDescription>
                        <ServiceType>STANDARD_OVERNIGHT</ServiceType>
                        <Code>05</Code>
                        <Names>
                            <Type>long</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>FedEx Standard OvernightÂ®</Value>
                        </Names>
                        <Names>
                            <Type>long</Type>
                            <Encoding>ascii</Encoding>
                            <Value>FedEx Standard Overnight</Value>
                        </Names>
                        <Names>
                            <Type>medium</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>FedEx Standard OvernightÂ®</Value>
                        </Names>
                        <Names>
                            <Type>medium</Type>
                            <Encoding>ascii</Encoding>
                            <Value>FedEx Standard Overnight</Value>
                        </Names>
                        <Names>
                            <Type>short</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>SOS</Value>
                        </Names>
                        <Names>
                            <Type>short</Type>
                            <Encoding>ascii</Encoding>
                            <Value>SOS</Value>
                        </Names>
                        <Names>
                            <Type>abbrv</Type>
                            <Encoding>ascii</Encoding>
                            <Value>SO</Value>
                        </Names>
                        <Description>Standard Overnight</Description>
                        <AstraDescription>STD OVR</AstraDescription>
                    </ServiceDescription>
                    <DerivedShipmentSignatureOption>
                        <OptionType>SERVICE_DEFAULT</OptionType>
                    </DerivedShipmentSignatureOption>
                    <DerivedOriginDetail>
                        <CountryCode>CA</CountryCode>
                        <StateOrProvinceCode>PQ</StateOrProvinceCode>
                        <PostalCode>J7H1H5</PostalCode>
                        <ServiceArea>A2</ServiceArea>
                        <LocationId>YMXA </LocationId>
                        <LocationNumber>0</LocationNumber>
                    </DerivedOriginDetail>
                    <DerivedDestinationDetail>
                        <CountryCode>CA</CountryCode>
                        <StateOrProvinceCode>BC</StateOrProvinceCode>
                        <PostalCode>V6M2V9</PostalCode>
                        <ServiceArea>A2</ServiceArea>
                        <LocationId>YVRA </LocationId>
                        <LocationNumber>0</LocationNumber>
                        <AirportId>YVR</AirportId>
                    </DerivedDestinationDetail>
                    <CommitTimestamp>2021-06-18T17:00:00</CommitTimestamp>
                    <DayOfWeek>FRI</DayOfWeek>
                    <DestinationServiceArea>A2</DestinationServiceArea>
                    <BrokerToDestinationDays>0</BrokerToDestinationDays>
                    <DocumentContent>NON_DOCUMENTS</DocumentContent>
                </CommitDetails>
                <DestinationAirportId>YVR</DestinationAirportId>
                <IneligibleForMoneyBackGuarantee>false</IneligibleForMoneyBackGuarantee>
                <OriginServiceArea>A2</OriginServiceArea>
                <DestinationServiceArea>A2</DestinationServiceArea>
                <SignatureOption>SERVICE_DEFAULT</SignatureOption>
                <ActualRateType>PAYOR_ACCOUNT_SHIPMENT</ActualRateType>
                <RatedShipmentDetails>
                    <EffectiveNetDiscount>
                        <Currency>CAD</Currency>
                        <Amount>41.63</Amount>
                    </EffectiveNetDiscount>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_ACCOUNT_SHIPMENT</RateType>
                        <RateScale>0000000</RateScale>
                        <RateZone>R0025</RateZone>
                        <PricingCode>ACTUAL</PricingCode>
                        <RatedWeightMethod>DIM</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>CAD</FromCurrency>
                            <IntoCurrency>CAD</IntoCurrency>
                            <Rate>1.0</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>166</DimDivisor>
                        <DimDivisorType>PRODUCT</DimDivisorType>
                        <FuelSurchargePercent>13.75</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>KG</Units>
                            <Value>14.4</Value>
                        </TotalBillingWeight>
                        <TotalDimWeight>
                            <Units>KG</Units>
                            <Value>14.4</Value>
                        </TotalDimWeight>
                        <TotalBaseCharge>
                            <Currency>CAD</Currency>
                            <Amount>208.55</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>CAD</Currency>
                            <Amount>208.55</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>CAD</Currency>
                            <Amount>21.51</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>CAD</Currency>
                            <Amount>230.06</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>CAD</Currency>
                            <Amount>11.5</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>CAD</Currency>
                            <Amount>241.56</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>241.56</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>21.51</Amount>
                            </Amount>
                        </Surcharges>
                        <Taxes>
                            <TaxType>GST</TaxType>
                            <Description>Canada freight goods and services</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>11.5</Amount>
                            </Amount>
                        </Taxes>
                    </ShipmentRateDetail>
                </RatedShipmentDetails>
                <RatedShipmentDetails>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_LIST_SHIPMENT</RateType>
                        <RateScale>0000000</RateScale>
                        <RateZone>R0025</RateZone>
                        <PricingCode>ACTUAL</PricingCode>
                        <RatedWeightMethod>DIM</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>CAD</FromCurrency>
                            <IntoCurrency>CAD</IntoCurrency>
                            <Rate>1.0</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>139</DimDivisor>
                        <DimDivisorType>COUNTRY</DimDivisorType>
                        <FuelSurchargePercent>13.75</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>KG</Units>
                            <Value>17.1</Value>
                        </TotalBillingWeight>
                        <TotalDimWeight>
                            <Units>KG</Units>
                            <Value>17.1</Value>
                        </TotalDimWeight>
                        <TotalBaseCharge>
                            <Currency>CAD</Currency>
                            <Amount>237.1</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>CAD</Currency>
                            <Amount>237.1</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>CAD</Currency>
                            <Amount>32.6</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>CAD</Currency>
                            <Amount>269.7</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>CAD</Currency>
                            <Amount>13.49</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>CAD</Currency>
                            <Amount>283.19</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>283.19</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>32.6</Amount>
                            </Amount>
                        </Surcharges>
                        <Taxes>
                            <TaxType>GST</TaxType>
                            <Description>Canada freight goods and services</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>13.49</Amount>
                            </Amount>
                        </Taxes>
                    </ShipmentRateDetail>
                </RatedShipmentDetails>
            </RateReplyDetails>
            <RateReplyDetails>
                <ServiceType>FEDEX_2_DAY</ServiceType>
                <ServiceDescription>
                    <ServiceType>FEDEX_2_DAY</ServiceType>
                    <Code>03</Code>
                    <Names>
                        <Type>long</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FedEx 2DayÂ®</Value>
                    </Names>
                    <Names>
                        <Type>long</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FedEx 2Day</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FedEx 2DayÂ®</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FedEx 2Day</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>P-2</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>ascii</Encoding>
                        <Value>P-2</Value>
                    </Names>
                    <Names>
                        <Type>abbrv</Type>
                        <Encoding>ascii</Encoding>
                        <Value>ES</Value>
                    </Names>
                    <Description>2Day</Description>
                    <AstraDescription>E2</AstraDescription>
                </ServiceDescription>
                <PackagingType>YOUR_PACKAGING</PackagingType>
                <DeliveryStation>YVRA </DeliveryStation>
                <DeliveryDayOfWeek>MON</DeliveryDayOfWeek>
                <CommitDetails>
                    <ServiceType>FEDEX_2_DAY</ServiceType>
                    <ServiceDescription>
                        <ServiceType>FEDEX_2_DAY</ServiceType>
                        <Code>03</Code>
                        <Names>
                            <Type>long</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>FedEx 2DayÂ®</Value>
                        </Names>
                        <Names>
                            <Type>long</Type>
                            <Encoding>ascii</Encoding>
                            <Value>FedEx 2Day</Value>
                        </Names>
                        <Names>
                            <Type>medium</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>FedEx 2DayÂ®</Value>
                        </Names>
                        <Names>
                            <Type>medium</Type>
                            <Encoding>ascii</Encoding>
                            <Value>FedEx 2Day</Value>
                        </Names>
                        <Names>
                            <Type>short</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>P-2</Value>
                        </Names>
                        <Names>
                            <Type>short</Type>
                            <Encoding>ascii</Encoding>
                            <Value>P-2</Value>
                        </Names>
                        <Names>
                            <Type>abbrv</Type>
                            <Encoding>ascii</Encoding>
                            <Value>ES</Value>
                        </Names>
                        <Description>2Day</Description>
                        <AstraDescription>E2</AstraDescription>
                    </ServiceDescription>
                    <DerivedShipmentSignatureOption>
                        <OptionType>SERVICE_DEFAULT</OptionType>
                    </DerivedShipmentSignatureOption>
                    <DerivedOriginDetail>
                        <CountryCode>CA</CountryCode>
                        <StateOrProvinceCode>PQ</StateOrProvinceCode>
                        <PostalCode>J7H1H5</PostalCode>
                        <ServiceArea>A2</ServiceArea>
                        <LocationId>YMXA </LocationId>
                        <LocationNumber>0</LocationNumber>
                    </DerivedOriginDetail>
                    <DerivedDestinationDetail>
                        <CountryCode>CA</CountryCode>
                        <StateOrProvinceCode>BC</StateOrProvinceCode>
                        <PostalCode>V6M2V9</PostalCode>
                        <ServiceArea>A2</ServiceArea>
                        <LocationId>YVRA </LocationId>
                        <LocationNumber>0</LocationNumber>
                        <AirportId>YVR</AirportId>
                    </DerivedDestinationDetail>
                    <CommitTimestamp>2021-06-21T17:00:00</CommitTimestamp>
                    <DayOfWeek>MON</DayOfWeek>
                    <DestinationServiceArea>A2</DestinationServiceArea>
                    <BrokerToDestinationDays>0</BrokerToDestinationDays>
                    <DocumentContent>NON_DOCUMENTS</DocumentContent>
                </CommitDetails>
                <DestinationAirportId>YVR</DestinationAirportId>
                <IneligibleForMoneyBackGuarantee>false</IneligibleForMoneyBackGuarantee>
                <OriginServiceArea>A2</OriginServiceArea>
                <DestinationServiceArea>A2</DestinationServiceArea>
                <SignatureOption>SERVICE_DEFAULT</SignatureOption>
                <ActualRateType>PAYOR_ACCOUNT_SHIPMENT</ActualRateType>
                <RatedShipmentDetails>
                    <EffectiveNetDiscount>
                        <Currency>CAD</Currency>
                        <Amount>141.04</Amount>
                    </EffectiveNetDiscount>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_ACCOUNT_SHIPMENT</RateType>
                        <RateScale>0000000</RateScale>
                        <RateZone>R0025</RateZone>
                        <PricingCode>ACTUAL</PricingCode>
                        <RatedWeightMethod>DIM</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>CAD</FromCurrency>
                            <IntoCurrency>CAD</IntoCurrency>
                            <Rate>1.0</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>166</DimDivisor>
                        <DimDivisorType>PRODUCT</DimDivisorType>
                        <FuelSurchargePercent>13.75</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>KG</Units>
                            <Value>14.4</Value>
                        </TotalBillingWeight>
                        <TotalDimWeight>
                            <Units>KG</Units>
                            <Value>14.4</Value>
                        </TotalDimWeight>
                        <TotalBaseCharge>
                            <Currency>CAD</Currency>
                            <Amount>195.2</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>CAD</Currency>
                            <Amount>87.84</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>CAD</Currency>
                            <Amount>107.36</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>CAD</Currency>
                            <Amount>11.07</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>CAD</Currency>
                            <Amount>118.43</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>CAD</Currency>
                            <Amount>5.92</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>CAD</Currency>
                            <Amount>124.35</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>124.35</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <FreightDiscounts>
                            <RateDiscountType>VOLUME</RateDiscountType>
                            <Description>Volume</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>87.84</Amount>
                            </Amount>
                            <Percent>45.0</Percent>
                        </FreightDiscounts>
                        <FreightDiscounts>
                            <RateDiscountType>OTHER</RateDiscountType>
                            <Description>Other</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>0.0</Amount>
                            </Amount>
                            <Percent>0.0</Percent>
                        </FreightDiscounts>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>11.07</Amount>
                            </Amount>
                        </Surcharges>
                        <Taxes>
                            <TaxType>GST</TaxType>
                            <Description>Canada freight goods and services</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>5.92</Amount>
                            </Amount>
                        </Taxes>
                    </ShipmentRateDetail>
                </RatedShipmentDetails>
                <RatedShipmentDetails>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_LIST_SHIPMENT</RateType>
                        <RateScale>0000000</RateScale>
                        <RateZone>R0025</RateZone>
                        <PricingCode>ACTUAL</PricingCode>
                        <RatedWeightMethod>DIM</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>CAD</FromCurrency>
                            <IntoCurrency>CAD</IntoCurrency>
                            <Rate>1.0</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>139</DimDivisor>
                        <DimDivisorType>COUNTRY</DimDivisorType>
                        <FuelSurchargePercent>13.75</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>KG</Units>
                            <Value>17.1</Value>
                        </TotalBillingWeight>
                        <TotalDimWeight>
                            <Units>KG</Units>
                            <Value>17.1</Value>
                        </TotalDimWeight>
                        <TotalBaseCharge>
                            <Currency>CAD</Currency>
                            <Amount>222.2</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>CAD</Currency>
                            <Amount>222.2</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>CAD</Currency>
                            <Amount>30.55</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>CAD</Currency>
                            <Amount>252.75</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>CAD</Currency>
                            <Amount>12.64</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>CAD</Currency>
                            <Amount>265.39</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>265.39</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>30.55</Amount>
                            </Amount>
                        </Surcharges>
                        <Taxes>
                            <TaxType>GST</TaxType>
                            <Description>Canada freight goods and services</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>12.64</Amount>
                            </Amount>
                        </Taxes>
                    </ShipmentRateDetail>
                </RatedShipmentDetails>
            </RateReplyDetails>
            <RateReplyDetails>
                <ServiceType>FEDEX_EXPRESS_SAVER</ServiceType>
                <ServiceDescription>
                    <ServiceType>FEDEX_EXPRESS_SAVER</ServiceType>
                    <Code>20</Code>
                    <Names>
                        <Type>long</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FedEx Economy</Value>
                    </Names>
                    <Names>
                        <Type>long</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FedEx Economy</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FedEx Economy</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FedEx Economy</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>XS</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>ascii</Encoding>
                        <Value>XS</Value>
                    </Names>
                    <Names>
                        <Type>abbrv</Type>
                        <Encoding>ascii</Encoding>
                        <Value>XS</Value>
                    </Names>
                    <Description>FedEx Economy</Description>
                    <AstraDescription>XS</AstraDescription>
                </ServiceDescription>
                <PackagingType>YOUR_PACKAGING</PackagingType>
                <DeliveryStation>YVRA </DeliveryStation>
                <DeliveryDayOfWeek>TUE</DeliveryDayOfWeek>
                <CommitDetails>
                    <ServiceType>FEDEX_EXPRESS_SAVER</ServiceType>
                    <ServiceDescription>
                        <ServiceType>FEDEX_EXPRESS_SAVER</ServiceType>
                        <Code>20</Code>
                        <Names>
                            <Type>long</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>FedEx Economy</Value>
                        </Names>
                        <Names>
                            <Type>long</Type>
                            <Encoding>ascii</Encoding>
                            <Value>FedEx Economy</Value>
                        </Names>
                        <Names>
                            <Type>medium</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>FedEx Economy</Value>
                        </Names>
                        <Names>
                            <Type>medium</Type>
                            <Encoding>ascii</Encoding>
                            <Value>FedEx Economy</Value>
                        </Names>
                        <Names>
                            <Type>short</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>XS</Value>
                        </Names>
                        <Names>
                            <Type>short</Type>
                            <Encoding>ascii</Encoding>
                            <Value>XS</Value>
                        </Names>
                        <Names>
                            <Type>abbrv</Type>
                            <Encoding>ascii</Encoding>
                            <Value>XS</Value>
                        </Names>
                        <Description>FedEx Economy</Description>
                        <AstraDescription>XS</AstraDescription>
                    </ServiceDescription>
                    <DerivedShipmentSignatureOption>
                        <OptionType>SERVICE_DEFAULT</OptionType>
                    </DerivedShipmentSignatureOption>
                    <DerivedOriginDetail>
                        <CountryCode>CA</CountryCode>
                        <StateOrProvinceCode>PQ</StateOrProvinceCode>
                        <PostalCode>J7H1H5</PostalCode>
                        <ServiceArea>A2</ServiceArea>
                        <LocationId>YMXA </LocationId>
                        <LocationNumber>0</LocationNumber>
                    </DerivedOriginDetail>
                    <DerivedDestinationDetail>
                        <CountryCode>CA</CountryCode>
                        <StateOrProvinceCode>BC</StateOrProvinceCode>
                        <PostalCode>V6M2V9</PostalCode>
                        <ServiceArea>A2</ServiceArea>
                        <LocationId>YVRA </LocationId>
                        <LocationNumber>0</LocationNumber>
                        <AirportId>YVR</AirportId>
                    </DerivedDestinationDetail>
                    <CommitTimestamp>2021-06-22T17:00:00</CommitTimestamp>
                    <DayOfWeek>TUE</DayOfWeek>
                    <DestinationServiceArea>A2</DestinationServiceArea>
                    <BrokerToDestinationDays>0</BrokerToDestinationDays>
                    <DocumentContent>NON_DOCUMENTS</DocumentContent>
                </CommitDetails>
                <DestinationAirportId>YVR</DestinationAirportId>
                <IneligibleForMoneyBackGuarantee>false</IneligibleForMoneyBackGuarantee>
                <OriginServiceArea>A2</OriginServiceArea>
                <DestinationServiceArea>A2</DestinationServiceArea>
                <SignatureOption>SERVICE_DEFAULT</SignatureOption>
                <ActualRateType>PAYOR_ACCOUNT_SHIPMENT</ActualRateType>
                <RatedShipmentDetails>
                    <EffectiveNetDiscount>
                        <Currency>CAD</Currency>
                        <Amount>138.42</Amount>
                    </EffectiveNetDiscount>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_ACCOUNT_SHIPMENT</RateType>
                        <RateScale>0000000</RateScale>
                        <RateZone>R0025</RateZone>
                        <PricingCode>ACTUAL</PricingCode>
                        <RatedWeightMethod>DIM</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>CAD</FromCurrency>
                            <IntoCurrency>CAD</IntoCurrency>
                            <Rate>1.0</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>166</DimDivisor>
                        <DimDivisorType>PRODUCT</DimDivisorType>
                        <FuelSurchargePercent>13.75</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>KG</Units>
                            <Value>14.4</Value>
                        </TotalBillingWeight>
                        <TotalDimWeight>
                            <Units>KG</Units>
                            <Value>14.4</Value>
                        </TotalDimWeight>
                        <TotalBaseCharge>
                            <Currency>CAD</Currency>
                            <Amount>124.7</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>CAD</Currency>
                            <Amount>97.27</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>CAD</Currency>
                            <Amount>27.43</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>CAD</Currency>
                            <Amount>2.83</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>CAD</Currency>
                            <Amount>30.26</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>CAD</Currency>
                            <Amount>1.51</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>CAD</Currency>
                            <Amount>31.77</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>31.77</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <FreightDiscounts>
                            <RateDiscountType>VOLUME</RateDiscountType>
                            <Description>Volume</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>97.27</Amount>
                            </Amount>
                            <Percent>78.0</Percent>
                        </FreightDiscounts>
                        <FreightDiscounts>
                            <RateDiscountType>OTHER</RateDiscountType>
                            <Description>Other</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>0.0</Amount>
                            </Amount>
                            <Percent>0.0</Percent>
                        </FreightDiscounts>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>2.83</Amount>
                            </Amount>
                        </Surcharges>
                        <Taxes>
                            <TaxType>GST</TaxType>
                            <Description>Canada freight goods and services</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>1.51</Amount>
                            </Amount>
                        </Taxes>
                    </ShipmentRateDetail>
                </RatedShipmentDetails>
                <RatedShipmentDetails>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_LIST_SHIPMENT</RateType>
                        <RateScale>0000000</RateScale>
                        <RateZone>R0025</RateZone>
                        <PricingCode>ACTUAL</PricingCode>
                        <RatedWeightMethod>DIM</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>CAD</FromCurrency>
                            <IntoCurrency>CAD</IntoCurrency>
                            <Rate>1.0</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>139</DimDivisor>
                        <DimDivisorType>COUNTRY</DimDivisorType>
                        <FuelSurchargePercent>13.75</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>KG</Units>
                            <Value>17.1</Value>
                        </TotalBillingWeight>
                        <TotalDimWeight>
                            <Units>KG</Units>
                            <Value>17.1</Value>
                        </TotalDimWeight>
                        <TotalBaseCharge>
                            <Currency>CAD</Currency>
                            <Amount>142.5</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>CAD</Currency>
                            <Amount>142.5</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>CAD</Currency>
                            <Amount>19.59</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>CAD</Currency>
                            <Amount>162.09</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>CAD</Currency>
                            <Amount>8.1</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>CAD</Currency>
                            <Amount>170.19</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>170.19</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>19.59</Amount>
                            </Amount>
                        </Surcharges>
                        <Taxes>
                            <TaxType>GST</TaxType>
                            <Description>Canada freight goods and services</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>8.1</Amount>
                            </Amount>
                        </Taxes>
                    </ShipmentRateDetail>
                </RatedShipmentDetails>
            </RateReplyDetails>
            <RateReplyDetails>
                <ServiceType>FEDEX_GROUND</ServiceType>
                <ServiceDescription>
                    <ServiceType>FEDEX_GROUND</ServiceType>
                    <Code>92</Code>
                    <Names>
                        <Type>long</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FedEx GroundÂ®</Value>
                    </Names>
                    <Names>
                        <Type>long</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FedEx Ground</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>GroundÂ®</Value>
                    </Names>
                    <Names>
                        <Type>medium</Type>
                        <Encoding>ascii</Encoding>
                        <Value>Ground</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>utf-8</Encoding>
                        <Value>FG</Value>
                    </Names>
                    <Names>
                        <Type>short</Type>
                        <Encoding>ascii</Encoding>
                        <Value>FG</Value>
                    </Names>
                    <Names>
                        <Type>abbrv</Type>
                        <Encoding>ascii</Encoding>
                        <Value>SG</Value>
                    </Names>
                    <Description>FedEx Ground</Description>
                    <AstraDescription>FXG</AstraDescription>
                </ServiceDescription>
                <PackagingType>YOUR_PACKAGING</PackagingType>
                <DeliveryDayOfWeek>THU</DeliveryDayOfWeek>
                <CommitDetails>
                    <ServiceType>FEDEX_GROUND</ServiceType>
                    <ServiceDescription>
                        <ServiceType>FEDEX_GROUND</ServiceType>
                        <Code>92</Code>
                        <Names>
                            <Type>long</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>FedEx GroundÂ®</Value>
                        </Names>
                        <Names>
                            <Type>long</Type>
                            <Encoding>ascii</Encoding>
                            <Value>FedEx Ground</Value>
                        </Names>
                        <Names>
                            <Type>medium</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>GroundÂ®</Value>
                        </Names>
                        <Names>
                            <Type>medium</Type>
                            <Encoding>ascii</Encoding>
                            <Value>Ground</Value>
                        </Names>
                        <Names>
                            <Type>short</Type>
                            <Encoding>utf-8</Encoding>
                            <Value>FG</Value>
                        </Names>
                        <Names>
                            <Type>short</Type>
                            <Encoding>ascii</Encoding>
                            <Value>FG</Value>
                        </Names>
                        <Names>
                            <Type>abbrv</Type>
                            <Encoding>ascii</Encoding>
                            <Value>SG</Value>
                        </Names>
                        <Description>FedEx Ground</Description>
                        <AstraDescription>FXG</AstraDescription>
                    </ServiceDescription>
                    <DerivedShipmentSignatureOption>
                        <OptionType>SERVICE_DEFAULT</OptionType>
                    </DerivedShipmentSignatureOption>
                    <DerivedOriginDetail>
                        <CountryCode>CA</CountryCode>
                        <StateOrProvinceCode>PQ</StateOrProvinceCode>
                        <PostalCode>J7H1H5</PostalCode>
                        <LocationNumber>6104</LocationNumber>
                    </DerivedOriginDetail>
                    <DerivedDestinationDetail>
                        <CountryCode>CA</CountryCode>
                        <StateOrProvinceCode>BC</StateOrProvinceCode>
                        <PostalCode>V6M2V9</PostalCode>
                        <LocationNumber>6227</LocationNumber>
                        <AirportId>YVR</AirportId>
                    </DerivedDestinationDetail>
                    <CommitTimestamp>2021-06-24T23:59:00</CommitTimestamp>
                    <DayOfWeek>THU</DayOfWeek>
                    <TransitTime>FIVE_DAYS</TransitTime>
                    <BrokerToDestinationDays>0</BrokerToDestinationDays>
                    <CommitMessages>
                        <Severity>NOTE</Severity>
                        <Source>vacs</Source>
                        <Code>2036</Code>
                        <Message>Time 23:59 = End of Day.</Message>
                    </CommitMessages>
                </CommitDetails>
                <DestinationAirportId>YVR</DestinationAirportId>
                <IneligibleForMoneyBackGuarantee>false</IneligibleForMoneyBackGuarantee>
                <TransitTime>FIVE_DAYS</TransitTime>
                <SignatureOption>SERVICE_DEFAULT</SignatureOption>
                <ActualRateType>PAYOR_ACCOUNT_SHIPMENT</ActualRateType>
                <RatedShipmentDetails>
                    <EffectiveNetDiscount>
                        <Currency>CAD</Currency>
                        <Amount>47.25</Amount>
                    </EffectiveNetDiscount>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_ACCOUNT_SHIPMENT</RateType>
                        <RateZone>6</RateZone>
                        <RatedWeightMethod>DIM</RatedWeightMethod>
                        <DimDivisor>139</DimDivisor>
                        <FuelSurchargePercent>13.75</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>LB</Units>
                            <Value>42.0</Value>
                        </TotalBillingWeight>
                        <TotalBaseCharge>
                            <Currency>CAD</Currency>
                            <Amount>27.99</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>CAD</Currency>
                            <Amount>27.99</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>CAD</Currency>
                            <Amount>3.85</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>CAD</Currency>
                            <Amount>31.84</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>CAD</Currency>
                            <Amount>1.59</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>CAD</Currency>
                            <Amount>33.43</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>33.43</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Level>PACKAGE</Level>
                            <Description>FedEx Ground Fuel</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>3.85</Amount>
                            </Amount>
                        </Surcharges>
                        <Taxes>
                            <TaxType>GST</TaxType>
                            <Description>Canada goods and services</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>1.59</Amount>
                            </Amount>
                        </Taxes>
                    </ShipmentRateDetail>
                    <RatedPackages>
                        <GroupNumber>0</GroupNumber>
                        <EffectiveNetDiscount>
                            <Currency>CAD</Currency>
                            <Amount>47.25</Amount>
                        </EffectiveNetDiscount>
                        <PackageRateDetail>
                            <RateType>PAYOR_ACCOUNT_SHIPMENT</RateType>
                            <RatedWeightMethod>DIM</RatedWeightMethod>
                            <BillingWeight>
                                <Units>KG</Units>
                                <Value>19.05</Value>
                            </BillingWeight>
                            <DimWeight>
                                <Units>KG</Units>
                                <Value>19.05</Value>
                            </DimWeight>
                            <BaseCharge>
                                <Currency>CAD</Currency>
                                <Amount>27.99</Amount>
                            </BaseCharge>
                            <TotalFreightDiscounts>
                                <Currency>CAD</Currency>
                                <Amount>0.0</Amount>
                            </TotalFreightDiscounts>
                            <NetFreight>
                                <Currency>CAD</Currency>
                                <Amount>27.99</Amount>
                            </NetFreight>
                            <TotalSurcharges>
                                <Currency>CAD</Currency>
                                <Amount>3.85</Amount>
                            </TotalSurcharges>
                            <NetFedExCharge>
                                <Currency>CAD</Currency>
                                <Amount>31.84</Amount>
                            </NetFedExCharge>
                            <TotalTaxes>
                                <Currency>CAD</Currency>
                                <Amount>1.59</Amount>
                            </TotalTaxes>
                            <NetCharge>
                                <Currency>CAD</Currency>
                                <Amount>33.43</Amount>
                            </NetCharge>
                            <TotalRebates>
                                <Currency>CAD</Currency>
                                <Amount>0.0</Amount>
                            </TotalRebates>
                            <Surcharges>
                                <SurchargeType>FUEL</SurchargeType>
                                <Level>PACKAGE</Level>
                                <Description>FedEx Ground Fuel</Description>
                                <Amount>
                                    <Currency>CAD</Currency>
                                    <Amount>3.85</Amount>
                                </Amount>
                            </Surcharges>
                            <Taxes>
                                <TaxType>GST</TaxType>
                                <Description>Canada goods and services</Description>
                                <Amount>
                                    <Currency>CAD</Currency>
                                    <Amount>1.59</Amount>
                                </Amount>
                            </Taxes>
                        </PackageRateDetail>
                    </RatedPackages>
                </RatedShipmentDetails>
                <RatedShipmentDetails>
                    <EffectiveNetDiscount>
                        <Currency>CAD</Currency>
                        <Amount>32.27</Amount>
                    </EffectiveNetDiscount>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_ACCOUNT_PACKAGE</RateType>
                        <RateZone>6</RateZone>
                        <RatedWeightMethod>DIM</RatedWeightMethod>
                        <DimDivisor>139</DimDivisor>
                        <FuelSurchargePercent>13.75</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>LB</Units>
                            <Value>42.0</Value>
                        </TotalBillingWeight>
                        <TotalDimWeight>
                            <Units>LB</Units>
                            <Value>42.0</Value>
                        </TotalDimWeight>
                        <TotalBaseCharge>
                            <Currency>CAD</Currency>
                            <Amount>67.55</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>CAD</Currency>
                            <Amount>27.02</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>CAD</Currency>
                            <Amount>40.53</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>CAD</Currency>
                            <Amount>5.57</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>CAD</Currency>
                            <Amount>46.1</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>CAD</Currency>
                            <Amount>2.31</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>CAD</Currency>
                            <Amount>48.41</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>48.41</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <FreightDiscounts>
                            <RateDiscountType>VOLUME</RateDiscountType>
                            <Description>Matrix</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>27.02</Amount>
                            </Amount>
                            <Percent>0.0</Percent>
                        </FreightDiscounts>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Level>PACKAGE</Level>
                            <Description>FedEx Ground Fuel</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>5.57</Amount>
                            </Amount>
                        </Surcharges>
                        <Taxes>
                            <TaxType>GST</TaxType>
                            <Description>Canada goods and services</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>2.31</Amount>
                            </Amount>
                        </Taxes>
                    </ShipmentRateDetail>
                    <RatedPackages>
                        <GroupNumber>0</GroupNumber>
                        <EffectiveNetDiscount>
                            <Currency>CAD</Currency>
                            <Amount>32.27</Amount>
                        </EffectiveNetDiscount>
                        <PackageRateDetail>
                            <RateType>PAYOR_ACCOUNT_PACKAGE</RateType>
                            <RatedWeightMethod>DIM</RatedWeightMethod>
                            <BillingWeight>
                                <Units>KG</Units>
                                <Value>19.05</Value>
                            </BillingWeight>
                            <DimWeight>
                                <Units>KG</Units>
                                <Value>19.05</Value>
                            </DimWeight>
                            <BaseCharge>
                                <Currency>CAD</Currency>
                                <Amount>67.55</Amount>
                            </BaseCharge>
                            <TotalFreightDiscounts>
                                <Currency>CAD</Currency>
                                <Amount>27.02</Amount>
                            </TotalFreightDiscounts>
                            <NetFreight>
                                <Currency>CAD</Currency>
                                <Amount>40.53</Amount>
                            </NetFreight>
                            <TotalSurcharges>
                                <Currency>CAD</Currency>
                                <Amount>5.57</Amount>
                            </TotalSurcharges>
                            <NetFedExCharge>
                                <Currency>CAD</Currency>
                                <Amount>46.1</Amount>
                            </NetFedExCharge>
                            <TotalTaxes>
                                <Currency>CAD</Currency>
                                <Amount>2.31</Amount>
                            </TotalTaxes>
                            <NetCharge>
                                <Currency>CAD</Currency>
                                <Amount>48.41</Amount>
                            </NetCharge>
                            <TotalRebates>
                                <Currency>CAD</Currency>
                                <Amount>0.0</Amount>
                            </TotalRebates>
                            <FreightDiscounts>
                                <RateDiscountType>VOLUME</RateDiscountType>
                                <Description>Matrix</Description>
                                <Amount>
                                    <Currency>CAD</Currency>
                                    <Amount>27.02</Amount>
                                </Amount>
                                <Percent>0.0</Percent>
                            </FreightDiscounts>
                            <Surcharges>
                                <SurchargeType>FUEL</SurchargeType>
                                <Level>PACKAGE</Level>
                                <Description>FedEx Ground Fuel</Description>
                                <Amount>
                                    <Currency>CAD</Currency>
                                    <Amount>5.57</Amount>
                                </Amount>
                            </Surcharges>
                            <Taxes>
                                <TaxType>GST</TaxType>
                                <Description>Canada goods and services</Description>
                                <Amount>
                                    <Currency>CAD</Currency>
                                    <Amount>2.31</Amount>
                                </Amount>
                            </Taxes>
                        </PackageRateDetail>
                    </RatedPackages>
                </RatedShipmentDetails>
                <RatedShipmentDetails>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_LIST_PACKAGE</RateType>
                        <RateZone>6</RateZone>
                        <RatedWeightMethod>DIM</RatedWeightMethod>
                        <DimDivisor>139</DimDivisor>
                        <FuelSurchargePercent>13.75</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>LB</Units>
                            <Value>42.0</Value>
                        </TotalBillingWeight>
                        <TotalDimWeight>
                            <Units>LB</Units>
                            <Value>42.0</Value>
                        </TotalDimWeight>
                        <TotalBaseCharge>
                            <Currency>CAD</Currency>
                            <Amount>67.55</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>CAD</Currency>
                            <Amount>67.55</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>CAD</Currency>
                            <Amount>9.29</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>CAD</Currency>
                            <Amount>76.84</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>CAD</Currency>
                            <Amount>3.84</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>CAD</Currency>
                            <Amount>80.68</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>CAD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>CAD</Currency>
                            <Amount>80.68</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Level>PACKAGE</Level>
                            <Description>FedEx Ground Fuel</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>9.29</Amount>
                            </Amount>
                        </Surcharges>
                        <Taxes>
                            <TaxType>GST</TaxType>
                            <Description>Canada goods and services</Description>
                            <Amount>
                                <Currency>CAD</Currency>
                                <Amount>3.84</Amount>
                            </Amount>
                        </Taxes>
                    </ShipmentRateDetail>
                    <RatedPackages>
                        <GroupNumber>0</GroupNumber>
                        <PackageRateDetail>
                            <RateType>PAYOR_LIST_PACKAGE</RateType>
                            <RatedWeightMethod>DIM</RatedWeightMethod>
                            <BillingWeight>
                                <Units>KG</Units>
                                <Value>19.05</Value>
                            </BillingWeight>
                            <DimWeight>
                                <Units>KG</Units>
                                <Value>19.05</Value>
                            </DimWeight>
                            <BaseCharge>
                                <Currency>CAD</Currency>
                                <Amount>67.55</Amount>
                            </BaseCharge>
                            <TotalFreightDiscounts>
                                <Currency>CAD</Currency>
                                <Amount>0.0</Amount>
                            </TotalFreightDiscounts>
                            <NetFreight>
                                <Currency>CAD</Currency>
                                <Amount>67.55</Amount>
                            </NetFreight>
                            <TotalSurcharges>
                                <Currency>CAD</Currency>
                                <Amount>9.29</Amount>
                            </TotalSurcharges>
                            <NetFedExCharge>
                                <Currency>CAD</Currency>
                                <Amount>76.84</Amount>
                            </NetFedExCharge>
                            <TotalTaxes>
                                <Currency>CAD</Currency>
                                <Amount>3.84</Amount>
                            </TotalTaxes>
                            <NetCharge>
                                <Currency>CAD</Currency>
                                <Amount>80.68</Amount>
                            </NetCharge>
                            <TotalRebates>
                                <Currency>CAD</Currency>
                                <Amount>0.0</Amount>
                            </TotalRebates>
                            <Surcharges>
                                <SurchargeType>FUEL</SurchargeType>
                                <Level>PACKAGE</Level>
                                <Description>FedEx Ground Fuel</Description>
                                <Amount>
                                    <Currency>CAD</Currency>
                                    <Amount>9.29</Amount>
                                </Amount>
                            </Surcharges>
                            <Taxes>
                                <TaxType>GST</TaxType>
                                <Description>Canada goods and services</Description>
                                <Amount>
                                    <Currency>CAD</Currency>
                                    <Amount>3.84</Amount>
                                </Amount>
                            </Taxes>
                        </PackageRateDetail>
                    </RatedPackages>
                </RatedShipmentDetails>
            </RateReplyDetails>
        </RateReply>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""
