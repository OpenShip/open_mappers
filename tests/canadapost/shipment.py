import unittest
from unittest.mock import patch
import purplship
from purplship.core.utils import DP
from purplship.core.models import ShipmentRequest, ShipmentCancelRequest
from tests.canadapost.fixture import gateway, LabelResponse


class TestCanadaPostShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)
        self.ShipmentCancelRequest = ShipmentCancelRequest(**shipment_cancel_data)

    def test_create_shipment_request(self):
        requests = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        pipeline = requests.serialize()
        request = pipeline["create_shipment"]()
        self.assertEqual(request.data.serialize(), ShipmentRequestXML)

    def test_create_shipment_with_package_preset_request(self):
        requests = gateway.mapper.create_shipment_request(
            ShipmentRequest(**shipment_with_package_preset_data)
        )
        pipeline = requests.serialize()
        request = pipeline["create_shipment"]()
        self.assertEqual(request.data.serialize(), ShipmentRequestWithPackagePresetXML)

    def test_create_non_contract_shipment_request(self):
        non_contract_gateway = purplship.gateway["canadapost"].create(
            dict(username="username", password="password", customer_number="2004381")
        )
        requests = non_contract_gateway.mapper.create_shipment_request(
            self.ShipmentRequest
        )
        pipeline = requests.serialize()
        request = pipeline["create_shipment"]()
        self.assertEqual(request.data.serialize(), NonContractShipmentRequestXML)

    def test_create_cancel_shipment_request(self):
        requests = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)
        pipeline = requests.serialize()
        info_request = pipeline["info"]()
        refund_request = pipeline["refund"](NonSubmittedShipmentResponseXML)
        # Assuming that the refund job will be skipped
        cancel_request = pipeline["cancel"](refund_request.fallback)

        self.assertEqual(info_request.data.serialize(), self.ShipmentCancelRequest.shipment_identifier)
        self.assertEqual(cancel_request.data.serialize(), self.ShipmentCancelRequest.shipment_identifier)

    def test_create_cancel_transmitted_shipment_request(self):
        requests = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)
        pipeline = requests.serialize()
        info_request = pipeline["info"]()
        refund_request = pipeline["refund"](ShipmentResponseXML)

        self.assertEqual(info_request.data.serialize(), self.ShipmentCancelRequest.shipment_identifier)
        self.assertEqual(refund_request.data["payload"].serialize(), ShipmentRefundRequestXML)

    def test_create_shipment(self):
        with patch("purplship.mappers.canadapost.proxy.http") as mocks:
            mocks.side_effect = ["<a></a>", ""]
            purplship.Shipment.create(self.ShipmentRequest).from_(gateway)

            create_call, _ = mocks.call_args_list
            self.assertEqual(
                create_call[1]["url"],
                f"{gateway.settings.server_url}/rs/{gateway.settings.customer_number}/{gateway.settings.customer_number}/shipment",
            )

    def test_cancel_shipment(self):
        with patch("purplship.mappers.canadapost.proxy.http") as mocks:
            mocks.side_effect = [NonSubmittedShipmentResponseXML, NonSubmittedShipmentResponseXML, ""]

            purplship.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            info_call, cancel_call = mocks.call_args_list
            self.assertEqual(
                info_call[1]["url"],
                f"{gateway.settings.server_url}/rs/2004381/2004381/shipment/123456789012",
            )
            self.assertEqual(
                cancel_call[1]["url"],
                f"{gateway.settings.server_url}/rs/2004381/2004381/shipment/123456789012",
            )

    def test_cancel_transmitted_shipment(self):
        with patch("purplship.mappers.canadapost.proxy.http") as mocks:
            mocks.side_effect = [ShipmentResponseXML, ShipmentRefundResponseXML, ""]

            purplship.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            info_call, refund_call = mocks.call_args_list
            self.assertEqual(
                info_call[1]["url"],
                f"{gateway.settings.server_url}/rs/2004381/2004381/shipment/123456789012",
            )
            self.assertEqual(
                refund_call[1]["url"],
                f"{gateway.settings.server_url}/rs/2004381/2004381/shipment/123456789012/refund",
            )

    def test_parse_shipment_response(self):
        with patch("purplship.mappers.canadapost.proxy.http") as mocks:
            mocks.side_effect = [ShipmentResponseXML, LabelResponse]
            parsed_response = (
                purplship.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertEqual(DP.to_dict(parsed_response), DP.to_dict(ParsedShipmentResponse))

    def test_parse_shipment_cancel_response(self):
        with patch("purplship.mappers.canadapost.proxy.http") as mocks:
            mocks.side_effect = [ShipmentResponseXML, ShipmentRefundResponseXML]
            parsed_response = (
                purplship.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedShipmentCancelResponse)
            )


if __name__ == "__main__":
    unittest.main()


shipment_cancel_data = {
    "shipment_identifier": "123456789012",
    "options": {"email": "test@test.com"}
}

shipment_data = {
    "shipper": {
        "company_name": "CGI",
        "address_line1": "502 MAIN ST N",
        "city": "MONTREAL",
        "postal_code": "H2B1A0",
        "country_code": "CA",
        "person_name": "Bob",
        "phone_number": "1 (450) 823-8432",
        "state_code": "QC",
    },
    "recipient": {
        "company_name": "CGI",
        "address_line1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "K1K 4T3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
    },
    "parcels": [
        {
            "height": 9,
            "length": 6,
            "width": 12,
            "weight": 20.0,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "service": "canadapost_expedited_parcel",
    "options": {
        "canadapost_signature": True,
        "cash_on_delivery": 10.5,
        "insurance": 70.0,
    },
    "reference": "#Order 11111",
}

shipment_with_package_preset_data = {
    "shipper": {
        "company_name": "CGI",
        "address_line1": "502 MAIN ST N",
        "city": "MONTREAL",
        "postal_code": "H2B1A0",
        "country_code": "CA",
        "person_name": "Bob",
        "phone_number": "1 (450) 823-8432",
        "state_code": "QC",
    },
    "recipient": {
        "company_name": "CGI",
        "address_line1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "K1K4T3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
    },
    "parcels": [
        {
            "weight": 20.0,
            "weight_unit": "LB",
            "package_preset": "canadapost_corrugated_large_box",
        }
    ],
    "service": "canadapost_expedited_parcel",
    "options": {"cash_on_delivery": 25.5},
    "label_type": "ZPL"
}

ParsedShipmentResponse = [
    {
        "carrier_name": "canadapost",
        "carrier_id": "canadapost",
        "label": LabelResponse,
        "tracking_number": "123456789012",
        "shipment_identifier": "123456789012",
    },
    [],
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "canadapost",
        "carrier_name": "canadapost",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]

ShipmentPriceLinkXML = """
<link rel="price" href="https://XX/rs/111111111/2222222222/shipment/347881315405043891/price" media-type="application/vnd.cpc.shipment-v8+xml" />
"""

ShipmentRequestXML = """<shipment xmlns="http://www.canadapost.ca/ws/shipment-v8">
    <transmit-shipment/>
    <requested-shipping-point>H2B1A0</requested-shipping-point>
    <provide-pricing-info>true</provide-pricing-info>
    <delivery-spec>
        <service-code>DOM.EP</service-code>
        <sender>
            <name>Bob</name>
            <company>CGI</company>
            <contact-phone>1 (450) 823-8432</contact-phone>
            <address-details>
                <address-line-1>502 MAIN ST N</address-line-1>
                <city>MONTREAL</city>
                <prov-state>QC</prov-state>
                <country-code>CA</country-code>
                <postal-zip-code>H2B1A0</postal-zip-code>
            </address-details>
        </sender>
        <destination>
            <name>Jain</name>
            <company>CGI</company>
            <address-details>
                <address-line-1>23 jardin private</address-line-1>
                <city>Ottawa</city>
                <prov-state>ON</prov-state>
                <country-code>CA</country-code>
                <postal-zip-code>K1K4T3</postal-zip-code>
            </address-details>
        </destination>
        <options>
            <option>
                <option-code>SO</option-code>
            </option>
            <option>
                <option-code>COD</option-code>
                <option-amount>10.5</option-amount>
            </option>
            <option>
                <option-code>COV</option-code>
                <option-amount>70.0</option-amount>
            </option>
        </options>
        <parcel-characteristics>
            <weight>20</weight>
            <dimensions>
                <length>6.0</length>
                <width>12.0</width>
                <height>9.0</height>
            </dimensions>
        </parcel-characteristics>
        <print-preferences>
            <output-format>4x6</output-format>
            <encoding>PDF</encoding>
        </print-preferences>
        <preferences>
            <show-packing-instructions>false</show-packing-instructions>
            <show-postage-rate>true</show-postage-rate>
            <show-insured-value>true</show-insured-value>
        </preferences>
        <references>
            <cost-centre>#Order 11111</cost-centre>
            <customer-ref-1>#Order 11111</customer-ref-1>
        </references>
        <settlement-info>
            <paid-by-customer>2004381</paid-by-customer>
            <contract-id>42708517</contract-id>
        </settlement-info>
    </delivery-spec>
</shipment>
"""

ShipmentRequestWithPackagePresetXML = """<shipment xmlns="http://www.canadapost.ca/ws/shipment-v8">
    <transmit-shipment/>
    <requested-shipping-point>H2B1A0</requested-shipping-point>
    <provide-pricing-info>true</provide-pricing-info>
    <delivery-spec>
        <service-code>DOM.EP</service-code>
        <sender>
            <name>Bob</name>
            <company>CGI</company>
            <contact-phone>1 (450) 823-8432</contact-phone>
            <address-details>
                <address-line-1>502 MAIN ST N</address-line-1>
                <city>MONTREAL</city>
                <prov-state>QC</prov-state>
                <country-code>CA</country-code>
                <postal-zip-code>H2B1A0</postal-zip-code>
            </address-details>
        </sender>
        <destination>
            <name>Jain</name>
            <company>CGI</company>
            <address-details>
                <address-line-1>23 jardin private</address-line-1>
                <city>Ottawa</city>
                <prov-state>ON</prov-state>
                <country-code>CA</country-code>
                <postal-zip-code>K1K4T3</postal-zip-code>
            </address-details>
        </destination>
        <options>
            <option>
                <option-code>COD</option-code>
                <option-amount>25.5</option-amount>
            </option>
        </options>
        <parcel-characteristics>
            <weight>9.1</weight>
            <dimensions>
                <length>40.6</length>
                <width>46.0</width>
                <height>46.0</height>
            </dimensions>
        </parcel-characteristics>
        <print-preferences>
            <output-format>4x6</output-format>
            <encoding>ZPL</encoding>
        </print-preferences>
        <preferences>
            <show-packing-instructions>false</show-packing-instructions>
            <show-postage-rate>true</show-postage-rate>
            <show-insured-value>true</show-insured-value>
        </preferences>
        <references>
            <cost-centre></cost-centre>
            <customer-ref-1></customer-ref-1>
        </references>
        <settlement-info>
            <paid-by-customer>2004381</paid-by-customer>
            <contract-id>42708517</contract-id>
        </settlement-info>
    </delivery-spec>
</shipment>
"""

NonContractShipmentRequestXML = """<non-contract-shipment xmlns="http://www.canadapost.ca/ws/ncshipment-v4">
    <delivery-spec>
        <service-code>DOM.EP</service-code>
        <sender>
            <name>Bob</name>
            <company>CGI</company>
            <contact-phone>1 (450) 823-8432</contact-phone>
            <address-details>
                <address-line-1>502 MAIN ST N</address-line-1>
                <city>MONTREAL</city>
                <prov-state>QC</prov-state>
                <postal-zip-code>H2B1A0</postal-zip-code>
            </address-details>
        </sender>
        <destination>
            <name>Jain</name>
            <company>CGI</company>
            <address-details>
                <address-line-1>23 jardin private</address-line-1>
                <city>Ottawa</city>
                <prov-state>ON</prov-state>
                <country-code>CA</country-code>
                <postal-zip-code>K1K4T3</postal-zip-code>
            </address-details>
        </destination>
        <options>
            <option>
                <option-code>SO</option-code>
            </option>
            <option>
                <option-code>COD</option-code>
                <option-amount>10.5</option-amount>
            </option>
            <option>
                <option-code>COV</option-code>
                <option-amount>70.0</option-amount>
            </option>
        </options>
        <parcel-characteristics>
            <weight>20</weight>
            <dimensions>
                <length>6.0</length>
                <width>12.0</width>
                <height>9.0</height>
            </dimensions>
        </parcel-characteristics>
        <preferences>
            <show-packing-instructions>false</show-packing-instructions>
            <show-postage-rate>true</show-postage-rate>
            <show-insured-value>true</show-insured-value>
        </preferences>
        <references>
            <cost-centre>#Order 11111</cost-centre>
            <customer-ref-1>#Order 11111</customer-ref-1>
        </references>
    </delivery-spec>
</non-contract-shipment>
"""

ShipmentResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<shipment-info xmlns="http://www.canadapost.ca/ws/shipment-v8">
  <shipment-id>545021584835957806</shipment-id>
  <shipment-status>transmitted</shipment-status>
  <tracking-pin>123456789012</tracking-pin>
  <po-number>P123456789</po-number>
  <shipment-price>
    <service-code>DOM.EP</service-code>
    <base-amount>25.07</base-amount>
    <priced-options>
      <priced-option>
        <option-code>DC</option-code>
        <option-price>0.00</option-price>
      </priced-option>
    </priced-options>
    <adjustments>
      <adjustment>
        <adjustment-code>FUELSC</adjustment-code>
        <adjustment-amount>2.88</adjustment-amount>
      </adjustment>
    </adjustments>
    <pre-tax-amount>27.95</pre-tax-amount>
    <gst-amount>0.00</gst-amount>
    <pst-amount>0.00</pst-amount>
    <hst-amount>3.63</hst-amount>
    <due-amount>31.58</due-amount>
    <service-standard>
      <am-delivery>false</am-delivery>
      <guaranteed-delivery>true</guaranteed-delivery>
      <expected-transmit-time>1</expected-transmit-time>
      <expected-delivery-date>2020-03-24</expected-delivery-date>
    </service-standard>
    <rated-weight>20.000</rated-weight>
  </shipment-price>
  <links>
    <link rel="self" href="https://ct.soa-gw.canadapost.ca/rs/0002004381/0002004381/shipment/545021584835957806" media-type="application/vnd.cpc.shipment-v8+xml"/>
    <link rel="details" href="https://ct.soa-gw.canadapost.ca/rs/0002004381/0002004381/shipment/545021584835957806/details" media-type="application/vnd.cpc.shipment-v8+xml"/>
    <link rel="refund" href="https://ct.soa-gw.canadapost.ca/rs/0002004381/0002004381/shipment/545021584835957806/refund" media-type="application/vnd.cpc.shipment-v8+xml"/>
    <link rel="label" href="https://ct.soa-gw.canadapost.ca/rs/artifact/6e93d53968881714/10001782951/0" media-type="application/pdf" index="0"/>
  </links>
</shipment-info>
"""

NonSubmittedShipmentResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<shipment-info xmlns="http://www.canadapost.ca/ws/shipment-v8">
  <shipment-id>545021584835957806</shipment-id>
  <shipment-status>created</shipment-status>
  <tracking-pin>123456789012</tracking-pin>
  <po-number>P123456789</po-number>
  <shipment-price>
    <service-code>DOM.EP</service-code>
    <base-amount>25.07</base-amount>
    <priced-options>
      <priced-option>
        <option-code>DC</option-code>
        <option-price>0.00</option-price>
      </priced-option>
    </priced-options>
    <adjustments>
      <adjustment>
        <adjustment-code>FUELSC</adjustment-code>
        <adjustment-amount>2.88</adjustment-amount>
      </adjustment>
    </adjustments>
    <pre-tax-amount>27.95</pre-tax-amount>
    <gst-amount>0.00</gst-amount>
    <pst-amount>0.00</pst-amount>
    <hst-amount>3.63</hst-amount>
    <due-amount>31.58</due-amount>
    <service-standard>
      <am-delivery>false</am-delivery>
      <guaranteed-delivery>true</guaranteed-delivery>
      <expected-transmit-time>1</expected-transmit-time>
      <expected-delivery-date>2020-03-24</expected-delivery-date>
    </service-standard>
    <rated-weight>20.000</rated-weight>
  </shipment-price>
  <links>
    <link rel="self" href="https://ct.soa-gw.canadapost.ca/rs/0002004381/0002004381/shipment/545021584835957806" media-type="application/vnd.cpc.shipment-v8+xml"/>
    <link rel="details" href="https://ct.soa-gw.canadapost.ca/rs/0002004381/0002004381/shipment/545021584835957806/details" media-type="application/vnd.cpc.shipment-v8+xml"/>
    <link rel="refund" href="https://ct.soa-gw.canadapost.ca/rs/0002004381/0002004381/shipment/545021584835957806/refund" media-type="application/vnd.cpc.shipment-v8+xml"/>
    <link rel="label" href="https://ct.soa-gw.canadapost.ca/rs/artifact/6e93d53968881714/10001782951/0" media-type="application/pdf" index="0"/>
  </links>
</shipment-info>
"""

ShipmentRefundRequestXML = """<shipment-refund-request xmlns="http://www.canadapost.ca/ws/shipment-v8">
    <email>test@test.com</email>
</shipment-refund-request>
"""

ShipmentRefundResponseXML = """<shipment-refund-request-info>
    <service-ticket-date>2015-01-28</service-ticket-date>
    <service-ticket-id>GT12345678RT</service-ticket-id>
</shipment-refund-request-info>
"""
