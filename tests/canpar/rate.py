import re
import time
import unittest
import logging
from unittest.mock import patch
from purplship.core.utils import DP
from purplship import Rating
from purplship.core.models import RateRequest
from tests.canpar.fixture import gateway


class TestCanparRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        serialized_request = re.sub(
            "<shipping_date>[^>]+</shipping_date>",
            "",
            request.serialize(),
        )

        self.assertEqual(serialized_request, RateRequestXML)

    def test_get_rates(self):
        with patch("purplship.mappers.canpar.proxy.http") as mock:
            mock.return_value = "<a></a>"
            Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/CanparRatingService.CanparRatingServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                mock.call_args[1]["headers"]["soapaction"], "urn:rateShipment"
            )

    def test_parse_rate_response(self):
        with patch("purplship.mappers.canpar.proxy.http") as mock:
            mock.return_value = RateResponseXml
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedQuoteResponse)
            )


if __name__ == "__main__":
    unittest.main()

RatePayload = {
    "shipper": {
        "company_name": "CGI",
        "address_line1": "502 MAIN ST N",
        "city": "MONTREAL",
        "postal_code": "H2B1A0",
        "country_code": "CA",
        "person_name": "Bob",
        "phone_number": "1 (450) 823-8432",
        "state_code": "QC",
        "residential": False,
    },
    "recipient": {
        "address_line1": "1 TEST ST",
        "city": "TORONTO",
        "company_name": "TEST ADDRESS",
        "phone_number": "4161234567",
        "postal_code": "M4X1W7",
        "state_code": "ON",
        "residential": False,
    },
    "parcels": [
        {
            "height": 3,
            "length": 10,
            "width": 3,
            "weight": 1.0,
        }
    ],
    "services": ["canpar_ground"],
    "options": {
        "canpar_extra_care": True,
    },
}

ParsedQuoteResponse = [
    [
        {
            "base_charge": 7.57,
            "carrier_id": "canpar",
            "carrier_name": "canpar",
            "currency": "CAD",
            "duties_and_taxes": 1.34,
            "extra_charges": [
                {"amount": 7.57, "currency": "CAD", "name": "Freight Charge"},
                {
                    "amount": 2.75,
                    "currency": "CAD",
                    "name": "Residential Address Surcharge",
                },
                {"amount": 1.34, "currency": "CAD", "name": "ONHST Tax Charge"},
            ],
            "meta": {"service_name": "canpar_ground"},
            "service": "canpar_ground",
            "total_charge": 11.66,
            "transit_days": 1,
        }
    ],
    [],
]


RateRequestXML = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"  xmlns:ws="http://ws.onlinerating.canshipws.canpar.com" xmlns:xsd="http://ws.dto.canshipws.canpar.com/xsd" xmlns:xsd1="http://dto.canshipws.canpar.com/xsd">
    <soap:Header/>
    <soap:Body>
        <ws:rateShipment>
            <ws:request>
                <xsd:apply_association_discount>false</xsd:apply_association_discount>
                <xsd:apply_individual_discount>false</xsd:apply_individual_discount>
                <xsd:apply_invoice_discount>false</xsd:apply_invoice_discount>
                <xsd:password>password</xsd:password>
                <xsd:shipment>
                    <xsd1:delivery_address>
                        <xsd1:address_line_1>1 TEST ST</xsd1:address_line_1>
                        <xsd1:address_line_2></xsd1:address_line_2>
                        <xsd1:city>TORONTO</xsd1:city>
                        <xsd1:name>TEST ADDRESS</xsd1:name>
                        <xsd1:phone>4161234567</xsd1:phone>
                        <xsd1:postal_code>M4X1W7</xsd1:postal_code>
                        <xsd1:province>ON</xsd1:province>
                        <xsd1:residential>false</xsd1:residential>
                    </xsd1:delivery_address>
                    <xsd1:dimention_unit>I</xsd1:dimention_unit>
                    <xsd1:packages>
                        <xsd1:height>7.62</xsd1:height>
                        <xsd1:length>25.399999999999999</xsd1:length>
                        <xsd1:reported_weight>1.</xsd1:reported_weight>
                        <xsd1:width>7.62</xsd1:width>
                        <xsd1:xc>true</xsd1:xc>
                    </xsd1:packages>
                    <xsd1:pickup_address>
                        <xsd1:address_line_1>502 MAIN ST N</xsd1:address_line_1>
                        <xsd1:address_line_2></xsd1:address_line_2>
                        <xsd1:attention>Bob</xsd1:attention>
                        <xsd1:city>MONTREAL</xsd1:city>
                        <xsd1:country>CA</xsd1:country>
                        <xsd1:name>CGI</xsd1:name>
                        <xsd1:phone>1 (450) 823-8432</xsd1:phone>
                        <xsd1:postal_code>H2B1A0</xsd1:postal_code>
                        <xsd1:province>QC</xsd1:province>
                        <xsd1:residential>false</xsd1:residential>
                    </xsd1:pickup_address>
                    <xsd1:reported_weight_unit>L</xsd1:reported_weight_unit>
                    <xsd1:service_type>1</xsd1:service_type>
                    <xsd1:shipping_date>{time.strftime('%Y-%m-%d')}T00:00:00</xsd1:shipping_date>
                </xsd:shipment>
                <xsd:user_id>user_id</xsd:user_id>
            </ws:request>
        </ws:rateShipment>
    </soap:Body>
</soap:Envelope>
"""

RateResponseXml = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
    <soapenv:Body>
        <ns:rateShipmentResponse xmlns:ns="http://ws.onlinerating.canshipws.canpar.com">
            <ns:return xmlns:ax25="http://ws.dto.canshipws.canpar.com/xsd" xmlns:ax27="http://dto.canshipws.canpar.com/xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ax25:RateShipmentRs">
                <ax25:error xsi:nil="true" />
                <ax25:processShipmentResult xsi:type="ax27:ProcessShipmentResult">
                    <ax27:shipment xsi:type="ax27:Shipment">
                        <ax27:airport_code />
                        <ax27:billed_weight>1.0</ax27:billed_weight>
                        <ax27:billed_weight_unit>L</ax27:billed_weight_unit>
                        <ax27:cod_charge>0.0</ax27:cod_charge>
                        <ax27:cod_type>N</ax27:cod_type>
                        <ax27:collect_shipper_num />
                        <ax27:consolidation_type />
                        <ax27:cos>false</ax27:cos>
                        <ax27:cos_charge>0.0</ax27:cos_charge>
                        <ax27:delivery_address xsi:type="ax27:Address">
                            <ax27:address_id>A1</ax27:address_id>
                            <ax27:address_line_1>1 TEST ST</ax27:address_line_1>
                            <ax27:address_line_2 />
                            <ax27:address_line_3 />
                            <ax27:attention />
                            <ax27:city>TORONTO</ax27:city>
                            <ax27:country>CA</ax27:country>
                            <ax27:email>1@1.COM,2@2.COM</ax27:email>
                            <ax27:extension>23</ax27:extension>
                            <ax27:id>-1</ax27:id>
                            <ax27:inserted_on>2012-06-15T15:42:39.278Z</ax27:inserted_on>
                            <ax27:name>TEST ADDRESS</ax27:name>
                            <ax27:phone>4161234567</ax27:phone>
                            <ax27:postal_code>M4X1W7</ax27:postal_code>
                            <ax27:province>ON</ax27:province>
                            <ax27:residential>false</ax27:residential>
                            <ax27:updated_on>2012-06-15T15:42:39.278Z</ax27:updated_on>
                        </ax27:delivery_address>
                        <ax27:description />
                        <ax27:dg>false</ax27:dg>
                        <ax27:dg_charge>0.0</ax27:dg_charge>
                        <ax27:dimention_unit>I</ax27:dimention_unit>
                        <ax27:dv_charge>0.0</ax27:dv_charge>
                        <ax27:ea_charge>0.0</ax27:ea_charge>
                        <ax27:ea_zone>0</ax27:ea_zone>
                        <ax27:estimated_delivery_date>2012-06-18T04:00:00.000Z</ax27:estimated_delivery_date>
                        <ax27:freight_charge>7.57</ax27:freight_charge>
                        <ax27:fuel_surcharge>0.0</ax27:fuel_surcharge>
                        <ax27:handling>0.0</ax27:handling>
                        <ax27:handling_type>$</ax27:handling_type>
                        <ax27:id>-1</ax27:id>
                        <ax27:inserted_on>2012-06-15T15:42:39.278Z</ax27:inserted_on>
                        <ax27:instruction />
                        <ax27:manifest_num xsi:nil="true" />
                        <ax27:nsr>false</ax27:nsr>
                        <ax27:packages xsi:type="ax27:Package">
                            <ax27:alternative_reference />
                            <ax27:barcode />
                            <ax27:billed_weight>1.0</ax27:billed_weight>
                            <ax27:cod xsi:nil="true" />
                            <ax27:cost_centre />
                            <ax27:declared_value>0.0</ax27:declared_value>
                            <ax27:dim_weight>0.0</ax27:dim_weight>
                            <ax27:dim_weight_flag>false</ax27:dim_weight_flag>
                            <ax27:height>0.0</ax27:height>
                            <ax27:id>-1</ax27:id>
                            <ax27:inserted_on>2012-06-15T15:42:39.278Z</ax27:inserted_on>
                            <ax27:length>0.0</ax27:length>
                            <ax27:min_weight_flag>false</ax27:min_weight_flag>
                            <ax27:package_num>0</ax27:package_num>
                            <ax27:package_reference>0</ax27:package_reference>
                            <ax27:reference />
                            <ax27:reported_weight>1.0</ax27:reported_weight>
                            <ax27:store_num />
                            <ax27:updated_on>2012-06-15T15:42:39.278Z</ax27:updated_on>
                            <ax27:width>0.0</ax27:width>
                            <ax27:xc>false</ax27:xc>
                        </ax27:packages>
                        <ax27:pickup_address xsi:type="ax27:Address">
                            <ax27:address_id>A1</ax27:address_id>
                            <ax27:address_line_1>1 TEST ST</ax27:address_line_1>
                            <ax27:address_line_2 />
                            <ax27:address_line_3 />
                            <ax27:attention />
                            <ax27:city>TORONTO</ax27:city>
                            <ax27:country>CA</ax27:country>
                            <ax27:email>1@1.COM,2@2.COM</ax27:email>
                            <ax27:extension>23</ax27:extension>
                            <ax27:id>-1</ax27:id>
                            <ax27:inserted_on>2012-06-15T15:42:39.278Z</ax27:inserted_on>
                            <ax27:name>TEST ADDRESS</ax27:name>
                            <ax27:phone>4161234567</ax27:phone>
                            <ax27:postal_code>M4X1W7</ax27:postal_code>
                            <ax27:province>ON</ax27:province>
                            <ax27:residential>false</ax27:residential>
                            <ax27:updated_on>2012-06-15T15:42:39.278Z</ax27:updated_on>
                        </ax27:pickup_address>
                        <ax27:premium>N</ax27:premium>
                        <ax27:premium_charge>0.0</ax27:premium_charge>
                        <ax27:proforma xsi:nil="true" />
                        <ax27:ra_charge>2.75</ax27:ra_charge>
                        <ax27:reported_weight_unit>L</ax27:reported_weight_unit>
                        <ax27:rural_charge>0.0</ax27:rural_charge>
                        <ax27:send_email_to_delivery>false</ax27:send_email_to_delivery>
                        <ax27:send_email_to_pickup>false</ax27:send_email_to_pickup>
                        <ax27:service_type>1</ax27:service_type>
                        <ax27:shipment_status>R</ax27:shipment_status>
                        <ax27:shipper_num>99999999</ax27:shipper_num>
                        <ax27:shipping_date>2012-06-15T04:00:00.000Z</ax27:shipping_date>
                        <ax27:tax_charge_1>1.34</ax27:tax_charge_1>
                        <ax27:tax_charge_2>0.0</ax27:tax_charge_2>
                        <ax27:tax_code_1>ONHST</ax27:tax_code_1>
                        <ax27:tax_code_2 />
                        <ax27:transit_time>1</ax27:transit_time>
                        <ax27:transit_time_guaranteed>false</ax27:transit_time_guaranteed>
                        <ax27:updated_on>2012-06-15T15:42:39.278Z</ax27:updated_on>
                        <ax27:user_id>WSADMIN@DEMO.COM</ax27:user_id>
                        <ax27:voided>false</ax27:voided>
                        <ax27:xc_charge>0.0</ax27:xc_charge>
                        <ax27:zone>1</ax27:zone>
                    </ax27:shipment>
                </ax25:processShipmentResult>
            </ns:return>
        </ns:rateShipmentResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""
