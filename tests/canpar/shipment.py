import re
import unittest
import time
from unittest.mock import patch
import purplship
from purplship.core.utils import DP
from purplship.core.models import ShipmentRequest, ShipmentCancelRequest
from tests.canpar.fixture import gateway


class TestCanparShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)
        self.VoidShipmentRequest = ShipmentCancelRequest(**void_shipment_data)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        pipeline = request.serialize()
        process_shipment_request = pipeline["process"]()
        get_label_request = pipeline["get_label"](ShipmentResponseXML)

        serialized_process_shipment_request = re.sub(
            "<shipping_date>[^>]+</shipping_date>",
            "",
            process_shipment_request.data.serialize(),
        )

        self.assertEqual(serialized_process_shipment_request, ShipmentRequestXML)
        self.assertEqual(get_label_request.data.serialize(), ShipmentLabelRequestXML)

    def test_create_void_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.VoidShipmentRequest
        )

        self.assertEqual(request.serialize(), VoidShipmentRequestXML)

    def test_create_shipment(self):
        with patch("purplship.mappers.canpar.proxy.http") as mocks:
            mocks.side_effect = [
                ShipmentResponseXML,
                ShipmentLabelResponseXML,
            ]
            purplship.Shipment.create(self.ShipmentRequest).from_(gateway)

            process_shipment_call, get_label_call = mocks.call_args_list

            self.assertEqual(
                process_shipment_call[1]["url"],
                f"{gateway.settings.server_url}/CanshipBusinessService.CanshipBusinessServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                process_shipment_call[1]["headers"]["soapaction"], "urn:processShipment"
            )
            self.assertEqual(
                get_label_call[1]["url"],
                f"{gateway.settings.server_url}/CanshipBusinessService.CanshipBusinessServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                get_label_call[1]["headers"]["soapaction"], "urn:getLabels"
            )

    def test_void_shipment(self):
        with patch("purplship.mappers.canpar.proxy.http") as mock:
            mock.return_value = "<a></a>"
            purplship.Shipment.cancel(self.VoidShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/CanshipBusinessService.CanshipBusinessServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                mock.call_args[1]["headers"]["soapaction"], "urn:voidShipment"
            )

    def test_parse_shipment_response(self):
        with patch("purplship.mappers.canpar.proxy.http") as mocks:
            mocks.side_effect = [
                ShipmentResponseXML,
                ShipmentLabelResponseXML,
            ]
            parsed_response = (
                purplship.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedShipmentResponse)
            )

    def test_parse_void_shipment_response(self):
        with patch("purplship.mappers.canpar.proxy.http") as mock:
            mock.return_value = VoidShipmentResponseXML
            parsed_response = (
                purplship.Shipment.cancel(self.VoidShipmentRequest)
                .from_(gateway)
                .parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedVoidShipmentResponse)
            )


if __name__ == "__main__":
    unittest.main()


void_shipment_data = {"shipment_identifier": "10000696"}

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
    "service": "canpar_ground",
    "options": {
        "canpar_extra_care": True,
    },
}

ParsedShipmentResponse = [
    {
        "carrier_id": "canpar",
        "carrier_name": "canpar",
        "label": "...ENCODED INFORMATION...",
        "selected_rate": {
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
        },
        "tracking_number": "D999999990000000461001",
        "shipment_identifier": "10000696",
    },
    [],
]

ParsedVoidShipmentResponse = [
    {
        "carrier_id": "canpar",
        "carrier_name": "canpar",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequestXML = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"  xmlns:ws="http://ws.onlinerating.canshipws.canpar.com" xmlns:xsd="http://ws.dto.canshipws.canpar.com/xsd" xmlns:xsd1="http://dto.canshipws.canpar.com/xsd">
    <soap:Header/>
    <soap:Body>
        <ws:processShipment>
            <ws:request>
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
        </ws:processShipment>
    </soap:Body>
</soap:Envelope>
"""

ShipmentLabelRequestXML = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"  xmlns:ws="http://ws.onlinerating.canshipws.canpar.com" xmlns:xsd="http://ws.dto.canshipws.canpar.com/xsd" >
    <soap:Header/>
    <soap:Body>
        <ws:getLabelsAdvanced>
            <ws:request>
                <xsd:horizontal>false</xsd:horizontal>
                <xsd:id>10000696</xsd:id>
                <xsd:password>password</xsd:password>
                <xsd:thermal>false</xsd:thermal>
                <xsd:user_id>user_id</xsd:user_id>
            </ws:request>
        </ws:getLabelsAdvanced>
    </soap:Body>
</soap:Envelope>
"""

ShipmentResponseXML = """<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
    <soapenv:Body>
        <ns:processShipmentResponse xmlns:ns="http://ws.business.canshipws.canpar.com">
            <ns:return xmlns:ax211="http://dto.canshipws.canpar.com/xsd"
                xmlns:ax29="http://ws.dto.canshipws.canpar.com/xsd"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ax29:ProcessShipmentRs">
                <ax29:error xsi:nil="true"/>
                <ax29:processShipmentResult xsi:type="ax211:ProcessShipmentResult">
                    <ax211:shipment xsi:type="ax211:Shipment">
                        <ax211:airport_code/>
                        <ax211:billed_weight>1.0</ax211:billed_weight>
                        <ax211:billed_weight_unit>L</ax211:billed_weight_unit>
                        <ax211:cod_charge>0.0</ax211:cod_charge>
                        <ax211:cod_type>N</ax211:cod_type>
                        <ax211:collect_shipper_num/>
                        <ax211:consolidation_type/>
                        <ax211:cos>false</ax211:cos>
                        <ax211:cos_charge>0.0</ax211:cos_charge>
                        <ax211:delivery_address xsi:type="ax211:Address">
                            <ax211:address_id>A1</ax211:address_id>
                            <ax211:address_line_1>1 TEST ST</ax211:address_line_1>
                            <ax211:address_line_2/>
                            <ax211:address_line_3/>
                            <ax211:attention/>
                            <ax211:city>TORONTO</ax211:city>
                            <ax211:country>CA</ax211:country>
                            <ax211:email>1@1.COM,2@2.COM</ax211:email>
                            <ax211:extension>23</ax211:extension>
                            <ax211:id>10001951</ax211:id>
                            <ax211:inserted_on>2012-06-15T15:41:11.763Z</ax211:inserted_on>
                            <ax211:name>TEST ADDRESS</ax211:name>
                            <ax211:phone>4161234567</ax211:phone>
                            <ax211:postal_code>M4X1W7</ax211:postal_code>
                            <ax211:province>ON</ax211:province>
                            <ax211:residential>false</ax211:residential>
                            <ax211:updated_on>2012-06-15T15:41:11.998Z</ax211:updated_on>
                        </ax211:delivery_address>
                        <ax211:description/>
                        <ax211:dg>false</ax211:dg>
                        <ax211:dg_charge>0.0</ax211:dg_charge>
                        <ax211:dimention_unit>I</ax211:dimention_unit>
                        <ax211:dv_charge>0.0</ax211:dv_charge>
                        <ax211:ea_charge>0.0</ax211:ea_charge>
                        <ax211:ea_zone>0</ax211:ea_zone>
                        <ax211:estimated_delivery_date>2012-06-18T04:00:00.000Z</ax211:estimated_delivery_date>
                        <ax211:freight_charge>7.57</ax211:freight_charge>
                        <ax211:fuel_surcharge>0.0</ax211:fuel_surcharge>
                        <ax211:handling>0.0</ax211:handling>
                        <ax211:handling_type>$</ax211:handling_type>
                        <ax211:id>10000696</ax211:id>
                        <ax211:inserted_on>2012-06-15T15:41:11.763Z</ax211:inserted_on>
                        <ax211:instruction/>
                        <ax211:manifest_num xsi:nil="true"/>
                        <ax211:nsr>false</ax211:nsr>
                        <ax211:packages xsi:type="ax211:Package">
                            <ax211:alternative_reference/>
                            <ax211:barcode>D999999990000000461001</ax211:barcode>
                            <ax211:billed_weight>1.0</ax211:billed_weight>
                            <ax211:cod xsi:nil="true"/>
                            <ax211:cost_centre/>
                            <ax211:declared_value>0.0</ax211:declared_value>
                            <ax211:dim_weight>0.0</ax211:dim_weight>
                            <ax211:dim_weight_flag>false</ax211:dim_weight_flag>
                            <ax211:height>0.0</ax211:height>
                            <ax211:id>10001802</ax211:id>
                            <ax211:inserted_on>2012-06-15T15:41:11.763Z</ax211:inserted_on>
                            <ax211:length>0.0</ax211:length>
                            <ax211:min_weight_flag>false</ax211:min_weight_flag>
                            <ax211:package_num>1</ax211:package_num>
                            <ax211:package_reference>461</ax211:package_reference>
                            <ax211:reference/>
                            <ax211:reported_weight>1.0</ax211:reported_weight>
                            <ax211:store_num/>
                            <ax211:updated_on>2012-06-15T15:41:11.998Z</ax211:updated_on>
                            <ax211:width>0.0</ax211:width>
                            <ax211:xc>false</ax211:xc>
                        </ax211:packages>
                        <ax211:pickup_address xsi:type="ax211:Address">
                            <ax211:address_id>A1</ax211:address_id>
                            <ax211:address_line_1>1 TEST ST</ax211:address_line_1>
                            <ax211:address_line_2/>
                            <ax211:address_line_3/>
                            <ax211:attention/>
                            <ax211:city>TORONTO</ax211:city>
                            <ax211:country>CA</ax211:country>
                            <ax211:email>1@1.COM,2@2.COM</ax211:email>
                            <ax211:extension>23</ax211:extension>
                            <ax211:id>10001950</ax211:id>
                            <ax211:inserted_on>2012-06-15T15:41:11.763Z</ax211:inserted_on>
                            <ax211:name>TEST ADDRESS</ax211:name>
                            <ax211:phone>4161234567</ax211:phone>
                            <ax211:postal_code>L6T0G8</ax211:postal_code>
                            <ax211:province>ON</ax211:province>
                            <ax211:residential>false</ax211:residential>
                            <ax211:updated_on>2012-06-15T15:41:11.998Z</ax211:updated_on>
                        </ax211:pickup_address>
                        <ax211:premium>N</ax211:premium>
                        <ax211:premium_charge>0.0</ax211:premium_charge>
                        <ax211:proforma xsi:nil="true"/>
                        <ax211:ra_charge>2.75</ax211:ra_charge>
                        <ax211:reported_weight_unit>L</ax211:reported_weight_unit>
                        <ax211:rural_charge>0.0</ax211:rural_charge>
                        <ax211:send_email_to_delivery>false</ax211:send_email_to_delivery>
                        <ax211:send_email_to_pickup>false</ax211:send_email_to_pickup>
                        <ax211:service_type>1</ax211:service_type>
                        <ax211:shipment_status>R</ax211:shipment_status>
                        <ax211:shipper_num>99999999</ax211:shipper_num>
                        <ax211:shipping_date>2012-06-15T04:00:00.000Z</ax211:shipping_date>
                        <ax211:tax_charge_1>1.34</ax211:tax_charge_1>
                        <ax211:tax_charge_2>0.0</ax211:tax_charge_2>
                        <ax211:tax_code_1>ONHST</ax211:tax_code_1>
                        <ax211:tax_code_2/>
                        <ax211:transit_time>1</ax211:transit_time>
                        <ax211:transit_time_guaranteed>false</ax211:transit_time_guaranteed>
                        <ax211:updated_on>2012-06-15T15:41:11.998Z</ax211:updated_on>
                        <ax211:user_id>user_id</ax211:user_id>
                        <ax211:voided>false</ax211:voided>
                        <ax211:xc_charge>0.0</ax211:xc_charge>
                        <ax211:zone>1</ax211:zone>
                    </ax211:shipment>
                </ax29:processShipmentResult>
            </ns:return>
        </ns:processShipmentResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentLabelResponseXML = """<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
    <soapenv:Body>
        <ns:getLabelsResponse xmlns:ns="http://ws.business.canshipws.canpar.com">
            <ns:return xmlns:ax211="http://dto.canshipws.canpar.com/xsd"
                xmlns:ax29="http://ws.dto.canshipws.canpar.com/xsd"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ax29:GetLabelsRs">
                <ax29:error xsi:nil="true"/>
                <ax29:labels>...ENCODED INFORMATION...</ax29:labels>
            </ns:return>
        </ns:getLabelsResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""

VoidShipmentRequestXML = """<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"  xmlns:ws="http://ws.onlinerating.canshipws.canpar.com" xmlns:xsd="http://ws.dto.canshipws.canpar.com/xsd" >
    <soap:Header/>
    <soap:Body>
        <ws:voidShipment>
            <ws:request>
                <xsd:id>10000696</xsd:id>
                <xsd:password>password</xsd:password>
                <xsd:user_id>user_id</xsd:user_id>
            </ws:request>
        </ws:voidShipment>
    </soap:Body>
</soap:Envelope>
"""

VoidShipmentResponseXML = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
    <soapenv:Body>
        <ns:voidShipmentResponse xmlns:ns="http://ws.business.canshipws.canpar.com">
            <ns:return xmlns:ax211="http://dto.canshipws.canpar.com/xsd"
                xmlns:ax29="http://ws.dto.canshipws.canpar.com/xsd"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ax29:VoidShipmentRs">
                <ax29:error xsi:nil="true"/>
            </ns:return>
        </ns:voidShipmentResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""
