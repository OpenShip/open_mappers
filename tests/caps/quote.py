import unittest
from unittest.mock import patch
from gds_helpers import to_xml, jsonify, export
from openship.domain.entities import Quote
from tests.caps.fixture import proxy
from tests.utils import strip


class TestCanadaPostQuote(unittest.TestCase):

    @patch("openship.mappers.caps.caps_proxy.http", return_value='<a></a>')
    def test_create_quote_request(self, http_mock):
        shipper = {"postal_code": "H8Z2Z3", "country_code": "CA"}
        recipient = {"postal_code": "H8Z2V4", "country_code": "CA"}
        shipment = {"packages": [{"weight": 4.0}]}
        payload = Quote.create(
            shipper=shipper, recipient=recipient, shipment=shipment)
        quote_req_xml_obj = proxy.mapper.create_quote_request(payload)

        proxy.get_quotes(quote_req_xml_obj)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        reqUrl = http_mock.call_args[1]['url']
        self.assertEqual(strip(xmlStr), strip(QuoteRequestXml))
        self.assertEqual(reqUrl, "%s/rs/ship/price" % (proxy.client.server_url))

    def test_parse_quote_response(self):
        parsed_response = proxy.mapper.parse_quote_response(
            to_xml(QuoteResponseXml))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedQuoteResponse))

    def test_parse_quote_parsing_error(self):
        parsed_response = proxy.mapper.parse_quote_response(
            to_xml(QuoteParsingError))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedQuoteParsingError))

    def test_parse_quote_missing_args_error(self):
        parsed_response = proxy.mapper.parse_quote_response(
            to_xml(QuoteMissingArgsError))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedQuoteMissingArgsError))


if __name__ == '__main__':
    unittest.main()


ParsedQuoteParsingError = [
    [], 
    [
        {
            'carrier': 'CanadaPost', 
            'code': 'AA004', 
            'message': 'You cannot mail on behalf of the requested customer.'
        }
    ]
]

ParsedQuoteMissingArgsError = [
    [], 
    [
        {
            'carrier': 'CanadaPost', 
            'code': 'Server', 
            'message': '/rs/ship/price: cvc-particle 3.1: in element {http://www.canadapost.ca/ws/ship/rate-v3}parcel-characteristics with anonymous type, found </parcel-characteristics> (in namespace http://www.canadapost.ca/ws/ship/rate-v3), but next item should be any of [{http://www.canadapost.ca/ws/ship/rate-v3}weight, {http://www.canadapost.ca/ws/ship/rate-v3}dimensions, {http://www.canadapost.ca/ws/ship/rate-v3}unpackaged, {http://www.canadapost.ca/ws/ship/rate-v3}mailing-tube, {http://www.canadapost.ca/ws/ship/rate-v3}oversized]'
        }
    ]
]

ParsedQuoteResponse = [
    [
        {
            'base_charge': 9.59, 
            'carrier': 'CanadaPost', 
            'delivery_date': '2011-10-24', 
            'delivery_time': None, 
            'discount': 0.6200000000000001, 
            'duties_and_taxes': 0.0, 
            'extra_charges': [
                {
                    'name': 'Automation discount', 
                    'amount': -0.29,
                    'currency': None
                }, 
                {
                    'name': 'Fuel surcharge', 
                    'amount': 0.91,
                    'currency': None
                }
            ], 
            'pickup_date': None, 
            'pickup_time': None, 
            'service_name': 'Expedited Parcel', 
            'service_type': 'DOM.EP', 
            'total_charge': 10.21
        }, 
        {
            'base_charge': 22.64, 
            'carrier': 'CanadaPost', 
            'delivery_date': '2011-10-21', 
            'delivery_time': None, 
            'discount': 2.56, 
            'duties_and_taxes': 0.0, 
            'extra_charges': [
                {
                    'name': 'Automation discount', 
                    'amount': -0.68,
                    'currency': None
                }, 
                {
                    'name': 'Fuel surcharge', 
                    'amount': 3.24,
                    'currency': None
                }
            ], 
            'pickup_date': None, 
            'pickup_time': None, 
            'service_name': 'Priority Courier', 
            'service_type': 'DOM.PC', 
            'total_charge': 25.2
        }, 
        {
            'base_charge': 9.59, 
            'carrier': 'CanadaPost', 
            'delivery_date': '2011-10-26', 
            'delivery_time': None, 
            'discount': 0.6200000000000001, 
            'duties_and_taxes': 0.0, 
            'extra_charges': [
                {
                    'name': 'Automation discount', 
                    'amount': -0.29,
                    'currency': None
                }, 
                {
                    'name': 'Fuel surcharge', 
                    'amount': 0.91,
                    'currency': None
                }
            ], 
            'pickup_date': None, 
            'pickup_time': None, 
            'service_name': 'Regular Parcel', 
            'service_type': 'DOM.RP', 
            'total_charge': 10.21
        }, 
        {
            'base_charge': 12.26, 
            'carrier': 'CanadaPost', 
            'delivery_date': '2011-10-24', 
            'delivery_time': None, 
            'discount': 1.38, 
            'duties_and_taxes': 0.0, 
            'extra_charges': [
                {
                    'name': 'Automation discount', 
                    'amount': -0.37,
                    'currency': None
                }, 
                {
                    'name': 'Fuel surcharge', 
                    'amount': 1.75,
                    'currency': None
                }
            ], 
            'pickup_date': None, 
            'pickup_time': None, 
            'service_name': 'Xpresspost', 
            'service_type': 'DOM.XP', 
            'total_charge': 13.64
        }
    ], 
    []
]


QuoteParsingError = """<messages xmlns="http://www.canadapost.ca/ws/messages">
    <message>
        <code>AA004</code>
        <description>You cannot mail on behalf of the requested customer.</description>
    </message>
</messages>
"""

QuoteMissingArgsError = """<messages xmlns="http://www.canadapost.ca/ws/messages">
    <message>
        <code>Server</code>
        <description>/rs/ship/price: cvc-particle 3.1: in element {http://www.canadapost.ca/ws/ship/rate-v3}parcel-characteristics with anonymous type, found &lt;/parcel-characteristics> (in namespace http://www.canadapost.ca/ws/ship/rate-v3), but next item should be any of [{http://www.canadapost.ca/ws/ship/rate-v3}weight, {http://www.canadapost.ca/ws/ship/rate-v3}dimensions, {http://www.canadapost.ca/ws/ship/rate-v3}unpackaged, {http://www.canadapost.ca/ws/ship/rate-v3}mailing-tube, {http://www.canadapost.ca/ws/ship/rate-v3}oversized]</description>
    </message>
</messages>
"""

QuoteRequestXml = """<mailing-scenario xmlns="http://www.canadapost.ca/ws/ship/rate-v3">
    <customer-number>1234567</customer-number>
    <parcel-characteristics>
        <weight>4.</weight>
        <dimensions/>
    </parcel-characteristics>
    <origin-postal-code>H8Z2Z3</origin-postal-code>
    <destination>
        <domestic>
            <postal-code>H8Z2V4</postal-code>
        </domestic>
    </destination>
</mailing-scenario>
"""

QuoteResponseXml = """<price-quotes>
   <price-quote>
      <service-code>DOM.EP</service-code>
      <service-link rel="service" href="https://ct.soa-gw.canadapost.ca/rs/ship/service/DOM.EP?country=CA" media-type="application/vnd.cpc.ship.rate-v3+xml" />
      <service-name>Expedited Parcel</service-name>
      <price-details>
         <base>9.59</base>
         <taxes>
            <gst>0.00</gst>
            <pst>0</pst>
            <hst>0</hst>
         </taxes>
         <due>10.21</due>
         <options>
            <option>
               <option-code>DC</option-code>
               <option-name>Delivery confirmation</option-name>
               <option-price>0</option-price>
            </option>
         </options>
         <adjustments>
            <adjustment>
               <adjustment-code>AUTDISC</adjustment-code>
               <adjustment-name>Automation discount</adjustment-name>
               <adjustment-cost>-0.29</adjustment-cost>
               <qualifier>
                  <percent>3.000</percent>
               </qualifier>
            </adjustment>
            <adjustment>
               <adjustment-code>FUELSC</adjustment-code>
               <adjustment-name>Fuel surcharge</adjustment-name>
               <adjustment-cost>0.91</adjustment-cost>
               <qualifier>
                  <percent>9.75</percent>
               </qualifier>
            </adjustment>
         </adjustments>
      </price-details>
      <weight-details />
      <service-standard>
         <am-delivery>false</am-delivery>
         <guaranteed-delivery>true</guaranteed-delivery>
         <expected-transit-time>2</expected-transit-time>
         <expected-delivery-date>2011-10-24</expected-delivery-date>
      </service-standard>
   </price-quote>
   <price-quote>
      <service-code>DOM.PC</service-code>
      <service-link rel="service" href="https://ct.soa-gw.canadapost.ca/rs/ship/service/DOM.PC?country=CA" media-type="application/vnd.cpc.ship.rate-v3+xml" />
      <service-name>Priority Courier</service-name>
      <price-details>
         <base>22.64</base>
         <taxes>
            <gst>0.00</gst>
            <pst>0</pst>
            <hst>0</hst>
         </taxes>
         <due>25.20</due>
         <options>
            <option>
               <option-code>DC</option-code>
               <option-name>Delivery confirmation</option-name>
               <option-price>0</option-price>
            </option>
         </options>
         <adjustments>
            <adjustment>
               <adjustment-code>AUTDISC</adjustment-code>
               <adjustment-name>Automation discount</adjustment-name>
               <adjustment-cost>-0.68</adjustment-cost>
               <qualifier>
                  <percent>3.000</percent>
               </qualifier>
            </adjustment>
            <adjustment>
               <adjustment-code>FUELSC</adjustment-code>
               <adjustment-name>Fuel surcharge</adjustment-name>
               <adjustment-cost>3.24</adjustment-cost>
               <qualifier>
                  <percent>14.75</percent>
               </qualifier>
            </adjustment>
         </adjustments>
      </price-details>
      <weight-details />
      <service-standard>
         <am-delivery>false</am-delivery>
         <guaranteed-delivery>true</guaranteed-delivery>
         <expected-transit-time>1</expected-transit-time>
         <expected-delivery-date>2011-10-21</expected-delivery-date>
      </service-standard>
   </price-quote>
   <price-quote>
      <service-code>DOM.RP</service-code>
      <service-link rel="service" href="https://ct.soa-gw.canadapost.ca/rs/ship/service/DOM.RP?country=CA" media-type="application/vnd.cpc.ship.rate-v3+xml" />
      <service-name>Regular Parcel</service-name>
      <price-details>
         <base>9.59</base>
         <taxes>
            <gst>0.00</gst>
            <pst>0</pst>
            <hst>0</hst>
         </taxes>
         <due>10.21</due>
         <options>
            <option>
               <option-code>DC</option-code>
               <option-name>Delivery confirmation</option-name>
               <option-price>0</option-price>
               <qualifier>
                  <included>true</included>
               </qualifier>
            </option>
         </options>
         <adjustments>
            <adjustment>
               <adjustment-code>AUTDISC</adjustment-code>
               <adjustment-name>Automation discount</adjustment-name>
               <adjustment-cost>-0.29</adjustment-cost>
               <qualifier>
                  <percent>3.000</percent>
               </qualifier>
            </adjustment>
            <adjustment>
               <adjustment-code>FUELSC</adjustment-code>
               <adjustment-name>Fuel surcharge</adjustment-name>
               <adjustment-cost>0.91</adjustment-cost>
               <qualifier>
                  <percent>9.75</percent>
               </qualifier>
            </adjustment>
         </adjustments>
      </price-details>
      <weight-details />
      <service-standard>
         <am-delivery>false</am-delivery>
         <guaranteed-delivery>false</guaranteed-delivery>
         <expected-transit-time>4</expected-transit-time>
         <expected-delivery-date>2011-10-26</expected-delivery-date>
      </service-standard>
   </price-quote>
   <price-quote>
      <service-code>DOM.XP</service-code>
      <service-link rel="service" href="https://ct.soa-gw.canadapost.ca/rs/ship/service/DOM.XP?country=CA" media-type="application/vnd.cpc.ship.rate-v3+xml" />
      <service-name>Xpresspost</service-name>
      <price-details>
         <base>12.26</base>
         <taxes>
            <gst>0.00</gst>
            <pst>0</pst>
            <hst>0</hst>
         </taxes>
         <due>13.64</due>
         <options>
            <option>
               <option-code>DC</option-code>
               <option-name>Delivery confirmation</option-name>
               <option-price>0</option-price>
            </option>
         </options>
         <adjustments>
            <adjustment>
               <adjustment-code>AUTDISC</adjustment-code>
               <adjustment-name>Automation discount</adjustment-name>
               <adjustment-cost>-0.37</adjustment-cost>
               <qualifier>
                  <percent>3.000</percent>
               </qualifier>
            </adjustment>
            <adjustment>
               <adjustment-code>FUELSC</adjustment-code>
               <adjustment-name>Fuel surcharge</adjustment-name>
               <adjustment-cost>1.75</adjustment-cost>
               <qualifier>
                  <percent>14.75</percent>
               </qualifier>
            </adjustment>
         </adjustments>
      </price-details>
      <weight-details />
      <service-standard>
         <am-delivery>false</am-delivery>
         <guaranteed-delivery>true</guaranteed-delivery>
         <expected-transit-time>2</expected-transit-time>
         <expected-delivery-date>2011-10-24</expected-delivery-date>
      </service-standard>
   </price-quote>
</price-quotes>
"""
