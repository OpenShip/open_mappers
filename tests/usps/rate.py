import unittest
import urllib.parse
from unittest.mock import patch
from purplship.core.utils import DP
from purplship.core.models import RateRequest
from purplship import Rating
from tests.usps.fixture import gateway


class TestUSPSRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RATE_PAYLOAD)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        self.assertEqual(request.serialize(), RATE_REQUEST_XML)

    @patch("purplship.mappers.usps.proxy.http", return_value="<a></a>")
    def test_get_rates(self, http_mock):
        Rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(
            url, f"{gateway.settings.server_url}?{urllib.parse.urlencode(RATE_REQUEST)}"
        )

    def test_parse_rate_response(self):
        with patch("purplship.mappers.usps.proxy.http") as mock:
            mock.return_value = RATE_RESPONSE_XML
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(PARSED_RATE_RESPONSE)
            )

    def test_parse_rate_response_errors(self):
        with patch("purplship.mappers.usps.proxy.http") as mock:
            mock.return_value = ERROR_XML
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(DP.to_dict(parsed_response), DP.to_dict(PARSED_ERRORS))


if __name__ == "__main__":
    unittest.main()


RATE_PAYLOAD = {
    "shipper": {"postal_code": "44106"},
    "recipient": {"postal_code": "20770"},
    "parcels": [
        {
            "width": 5,
            "height": 5,
            "length": 3,
            "weight": 1,
            "weight_unit": "LB",
            "dimension_unit": "IN",
        }
    ],
    "services": ["usps_priority"],
    "options": {"usps_signature_confirmation": True},
}

PARSED_RATE_RESPONSE = [
    [
        {
            "base_charge": 31.15,
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "meta": {"service_name": "usps_priority_mail_express"},
            "service": "usps_priority_mail_express",
            "total_charge": 31.15,
        },
        {
            "base_charge": 31.15,
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "meta": {"service_name": "usps_priority_mail_express_hold_for_pickup"},
            "service": "usps_priority_mail_express_hold_for_pickup",
            "total_charge": 31.15,
        },
        {
            "base_charge": 43.65,
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "meta": {
                "service_name": "usps_priority_mail_express_sunday_holiday_delivery"
            },
            "service": "usps_priority_mail_express_sunday_holiday_delivery",
            "total_charge": 43.65,
        },
        {
            "base_charge": 8.85,
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "meta": {"service_name": "usps_priority_mail"},
            "service": "usps_priority_mail",
            "total_charge": 8.85,
        },
        {
            "base_charge": 21.9,
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "meta": {"service_name": "usps_priority_mail_large_flat_rate_box"},
            "service": "usps_priority_mail_large_flat_rate_box",
            "total_charge": 21.9,
        },
        {
            "base_charge": 15.5,
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "meta": {"service_name": "usps_priority_mail_medium_flat_rate_box"},
            "service": "usps_priority_mail_medium_flat_rate_box",
            "total_charge": 15.5,
        },
        {
            "base_charge": 3.45,
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "meta": {"service_name": "usps_media_mail"},
            "service": "usps_media_mail",
            "total_charge": 3.45,
        },
        {
            "base_charge": 3.28,
            "carrier_id": "usps",
            "carrier_name": "usps",
            "currency": "USD",
            "meta": {"service_name": "usps_library_mail"},
            "service": "usps_library_mail",
            "total_charge": 3.28,
        },
    ],
    [],
]

PARSED_ERRORS = [
    [],
    [
        {
            "carrier_name": "usps",
            "carrier_id": "usps",
            "code": "-2147218040",
            "message": "Invalid International Mail Type",
        }
    ],
]


ERROR_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Error>
    <Number>-2147218040</Number>
    <Source>IntlPostage;clsIntlPostage.CalcAllPostageDimensionsXML;IntlRateV2.ProcessRequest</Source>
    <Description>Invalid International Mail Type</Description>
    <HelpFile />
    <HelpContext>1000440</HelpContext>
</Error>
"""

RATE_REQUEST_XML = """<RateV4Request USERID="username">
    <Revision>2</Revision>
    <Package ID="0">
        <Service>Priority</Service>
        <ZipOrigination>44106</ZipOrigination>
        <ZipDestination>20770</ZipDestination>
        <Pounds>1</Pounds>
        <Ounces>16</Ounces>
        <Container>VARIABLE</Container>
        <Width>5</Width>
        <Length>3</Length>
        <Height>5</Height>
        <Girth>40.64</Girth>
        <SpecialServices>
            <SpecialService>108</SpecialService>
        </SpecialServices>
        <Machinable>false</Machinable>
    </Package>
</RateV4Request>
"""

RATE_REQUEST = {"API": "RateV4", "XML": RATE_REQUEST_XML}

RATE_RESPONSE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<RateV4Response>
  <Package ID="0">
    <ZipOrigination>44106</ZipOrigination>
    <ZipDestination>20770</ZipDestination>
    <Pounds>1</Pounds>
    <Ounces>16.</Ounces>
    <Machinable>FALSE</Machinable>
    <Zone>3</Zone>
    <Postage CLASSID="3">
      <MailService>Priority Mail Express 2-Day&amp;lt;sup&amp;gt;&amp;#8482;&amp;lt;/sup&amp;gt;</MailService>
      <Rate>31.15</Rate>
      <CommitmentName>2-Day</CommitmentName>
    </Postage>
    <Postage CLASSID="2">
      <MailService>Priority Mail Express 2-Day&amp;lt;sup&amp;gt;&amp;#8482;&amp;lt;/sup&amp;gt; Hold For Pickup</MailService>
      <Rate>31.15</Rate>
      <CommitmentName>2-Day</CommitmentName>
    </Postage>
    <Postage CLASSID="23">
      <MailService>Priority Mail Express 2-Day&amp;lt;sup&amp;gt;&amp;#8482;&amp;lt;/sup&amp;gt; Sunday/Holiday Delivery</MailService>
      <Rate>43.65</Rate>
      <CommitmentName>2-Day</CommitmentName>
    </Postage>
    <Postage CLASSID="1">
      <MailService>Priority Mail 2-Day&amp;lt;sup&amp;gt;&amp;#8482;&amp;lt;/sup&amp;gt;</MailService>
      <Rate>8.85</Rate>
      <CommitmentName>2-Day</CommitmentName>
    </Postage>
    <Postage CLASSID="22">
      <MailService>Priority Mail 2-Day&amp;lt;sup&amp;gt;&amp;#8482;&amp;lt;/sup&amp;gt; Large Flat Rate Box</MailService>
      <Rate>21.90</Rate>
      <CommitmentName>2-Day</CommitmentName>
    </Postage>
    <Postage CLASSID="17">
      <MailService>Priority Mail 2-Day&amp;lt;sup&amp;gt;&amp;#8482;&amp;lt;/sup&amp;gt; Medium Flat Rate Box</MailService>
      <Rate>15.50</Rate>
      <CommitmentName>2-Day</CommitmentName>
    </Postage>
    <Postage CLASSID="6">
      <MailService>Media Mail Parcel</MailService>
      <Rate>3.45</Rate>
    </Postage>
    <Postage CLASSID="7">
      <MailService>Library Mail Parcel</MailService>
      <Rate>3.28</Rate>
    </Postage>
  </Package>
</RateV4Response>
"""
