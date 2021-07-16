import re
import unittest
from unittest.mock import patch
from purplship.core.utils import DP
from purplship.core.models import RateRequest
from purplship import Rating
from tests.usps_international.fixture import gateway


class TestUSPSRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RATE_PAYLOAD)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        serialized_request = re.sub(
            "<AcceptanceDateTime>[^>]+</AcceptanceDateTime>", "", request.serialize()
        )
        self.assertEqual(serialized_request, RATE_REQUEST_XML)

    def test_parse_rate_response(self):
        with patch("purplship.mappers.usps_international.proxy.http") as mock:
            mock.return_value = RATE_RESPONSE_XML
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(PARSED_RATE_RESPONSE)
            )

    def test_parse_rate_response_errors(self):
        with patch("purplship.mappers.usps_international.proxy.http") as mock:
            mock.return_value = ERROR_XML
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(DP.to_dict(parsed_response), DP.to_dict(PARSED_ERRORS))


if __name__ == "__main__":
    unittest.main()


RATE_PAYLOAD = {
    "shipper": {"postal_code": "18701"},
    "recipient": {"postal_code": "2046", "country_code": "AU"},
    "parcels": [
        {
            "width": 10,
            "height": 10,
            "length": 10,
            "weight": 3.123,
            "weight_unit": "LB",
            "dimension_unit": "IN",
        }
    ],
    "options": {"usps_insurance_global_express_guaranteed": True},
}

PARSED_RATE_RESPONSE = [
    [
        {
            "base_charge": 115.9,
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [{"amount": 0.0, "currency": "USD", "name": "Insurance"}],
            "service": "usps_global_express_guaranteed_envelopes",
            "total_charge": 115.9,
            "meta": {"service_name": "usps_global_express_guaranteed_envelopes"},
        },
        {
            "base_charge": 82.45,
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [{"amount": 0.0, "currency": "USD", "name": "Insurance"}],
            "service": "usps_priority_mail_express_international",
            "total_charge": 82.45,
            "meta": {"service_name": "usps_priority_mail_express_international"},
        },
        {
            "base_charge": 55.35,
            "carrier_id": "usps_international",
            "carrier_name": "usps_international",
            "currency": "USD",
            "extra_charges": [{"amount": 0.0, "currency": "USD", "name": "Insurance"}],
            "service": "usps_priority_mail_international",
            "total_charge": 55.35,
            "meta": {"service_name": "usps_priority_mail_international"},
        },
    ],
    [],
]

PARSED_ERRORS = [
    [],
    [
        {
            "carrier_name": "usps_international",
            "carrier_id": "usps_international",
            "code": "-2147219037",
            "message": "AcceptanceDateTime cannot be earlier than today's date.",
        }
    ],
]


ERROR_XML = """<?xml version="1.0" encoding="UTF-8"?>
<IntlRateV2Response>
  <Package ID="0">
    <Error>
      <Number>-2147219037</Number>
      <Source>;IntlRateV2.ProcessRequest</Source>
      <Description>AcceptanceDateTime cannot be earlier than today's date.</Description>
      <HelpFile/>
      <HelpContext/>
    </Error>
  </Package>
</IntlRateV2Response>
"""

RATE_REQUEST_XML = """<IntlRateV2Request USERID="username">
    <Revision>2</Revision>
    <Package ID="0">
        <Pounds>3</Pounds>
        <Ounces>49.97</Ounces>
        <Machinable>false</Machinable>
        <MailType>PACKAGE</MailType>
        <ValueOfContents></ValueOfContents>
        <Country>Australia</Country>
        <Width>10</Width>
        <Length>10</Length>
        <Height>10</Height>
        <OriginZip>18701</OriginZip>
        <CommercialFlag>N</CommercialFlag>
        <CommercialPlusFlag>N</CommercialPlusFlag>
        <ExtraServices>
            <ExtraService>106</ExtraService>
        </ExtraServices>
        
        <DestinationPostalCode>2046</DestinationPostalCode>
    </Package>
</IntlRateV2Request>
"""

RATE_REQUEST = {"API": "IntlRateV2", "XML": RATE_REQUEST_XML}

RATE_RESPONSE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<IntlRateV2Response>
  <Package ID="0">
    <AreasServed>Please reference Express Mail for Areas Served.</AreasServed>
    <AdditionalRestrictions>No Additional Restrictions Data found.</AdditionalRestrictions>
    <Service ID="12">
      <Pounds>3</Pounds>
      <Ounces>49.97</Ounces>
      <Machinable>false</Machinable>
      <MailType>PACKAGE</MailType>
      <Width>10.</Width>
      <Length>10.</Length>
      <Height>10.</Height>
      <Country>CANADA</Country>
      <Postage>115.90</Postage>
      <ExtraServices>
        <ExtraService>
          <ServiceID>106</ServiceID>
          <ServiceName>Insurance</ServiceName>
          <Available>True</Available>
          <Price>0.00</Price>
          <DeclaredValueRequired>True</DeclaredValueRequired>
        </ExtraService>
      </ExtraServices>
      <ValueOfContents>100.00</ValueOfContents>
      <SvcCommitments>1 - 3 business days to many major markets</SvcCommitments>
      <SvcDescription>USPS GXG&amp;lt;sup&amp;gt;&amp;#8482;&amp;lt;/sup&amp;gt; Envelopes</SvcDescription>
      <MaxDimensions>USPS-Produced regular size cardboard envelope (12-1/2" x 9-1/2"), the legal-sized cardboard envelope (15" x 9-1/2") and the GXG Tyvek envelope (15-1/2" x 12-1/2")</MaxDimensions>
      <MaxWeight>70</MaxWeight>
    </Service>
    <Service ID="1">
      <Pounds>3</Pounds>
      <Ounces>49.97</Ounces>
      <Machinable>false</Machinable>
      <MailType>PACKAGE</MailType>
      <Width>10.</Width>
      <Length>10.</Length>
      <Height>10.</Height>
      <Country>CANADA</Country>
      <Postage>82.45</Postage>
      <ExtraServices>
        <ExtraService>
          <ServiceID>107</ServiceID>
          <ServiceName>Insurance</ServiceName>
          <Available>True</Available>
          <Price>0.00</Price>
          <DeclaredValueRequired>True</DeclaredValueRequired>
        </ExtraService>
      </ExtraServices>
      <ValueOfContents>100.00</ValueOfContents>
      <SvcCommitments>Wed, Jun 09, 2021 Guaranteed</SvcCommitments>
      <SvcDescription>Priority Mail Express International&amp;lt;sup&amp;gt;&amp;#8482;&amp;lt;/sup&amp;gt;</SvcDescription>
      <MaxDimensions>Max. length 59", max. length plus girth 108"</MaxDimensions>
      <MaxWeight>66</MaxWeight>
    </Service>
    <Service ID="2">
      <Pounds>3</Pounds>
      <Ounces>49.97</Ounces>
      <Machinable>false</Machinable>
      <MailType>PACKAGE</MailType>
      <Width>10.</Width>
      <Length>10.</Length>
      <Height>10.</Height>
      <Country>CANADA</Country>
      <Postage>55.35</Postage>
      <ExtraServices>
        <ExtraService>
          <ServiceID>108</ServiceID>
          <ServiceName>Insurance</ServiceName>
          <Available>True</Available>
          <Price>0.00</Price>
          <DeclaredValueRequired>True</DeclaredValueRequired>
        </ExtraService>
      </ExtraServices>
      <ValueOfContents>100.00</ValueOfContents>
      <SvcCommitments>6 - 10 business days to many major markets</SvcCommitments>
      <SvcDescription>Priority Mail International&amp;lt;sup&amp;gt;&amp;#174;&amp;lt;/sup&amp;gt;</SvcDescription>
      <MaxDimensions>Max. length 79", max. length plus girth 108"</MaxDimensions>
      <MaxWeight>66</MaxWeight>
    </Service>
  </Package>
</IntlRateV2Response>
"""
