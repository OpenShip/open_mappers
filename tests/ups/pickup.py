import unittest
from unittest.mock import patch
import time
from gds_helpers import to_xml, jsonify, export
from pyups.freight_pickup import FreightPickupRequest, FreightCancelPickupRequest
from purplship.domain.entities import Shipment
from tests.ups.fixture import proxy
from tests.utils import strip, get_node_from_xml


class TestPickup(unittest.TestCase):
    def setUp(self):
        self.PickupRequest = FreightPickupRequest()
        self.PickupRequest.build(get_node_from_xml(PickupRequestXml, 'FreightPickupRequest'))

    @patch("purplship.mappers.ups.ups_proxy.http", return_value='<a></a>')
    def test_request_pickup(self, http_mock):
        proxy.request_pickup(self.PickupRequest)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(PickupRequestXml))


if __name__ == '__main__':
    unittest.main()

PickupRequestXml = """<tns:Envelope  xmlns:auth="http://www.ups.com/schema/xpci/1.0/auth" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upsa="http://www.ups.com/XMLSchema/XOLTWS/upssa/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:wsf="http://www.ups.com/schema/wsf" xmlns="http://www.ups.com/XMLSchema/XOLTWS/FreightPickup/v1.0" >
   <tns:Header>
        <upss:UPSSecurity>
            <upss:UsernameToken>
                <upss:Username>username</upss:Username>
                <upss:Password>password</upss:Password>
            </upss:UsernameToken>
            <upss:ServiceAccessToken>
                <upss:AccessLicenseNumber>FG09H9G8H09GH8G0</upss:AccessLicenseNumber>
            </upss:ServiceAccessToken>
        </upss:UPSSecurity>
   </tns:Header>
   <tns:Body>
      <FreightPickupRequest>
         <common:Request>
            <common:TransactionReference>
               <common:CustomerContext></common:CustomerContext>
            </common:TransactionReference>
         </common:Request>
         <DestinationPostalCode>DestinationPostalCode</DestinationPostalCode>
         <DestinationCountryCode>DestinationCountryCode</DestinationCountryCode>
         <Requester>
            <AttentionName>AttentionName</AttentionName>
            <EMailAddress>EMailAddress</EMailAddress>
            <Name>Name</Name>
            <Phone>
               <Number>Number</Number>
            </Phone>
         </Requester>
         <ShipFrom>
            <AttentionName>AttentionName</AttentionName>
            <Name>Name</Name>
            <Address>
               <AddressLine>AddressLine</AddressLine>
               <City>City</City>
               <StateProvinceCode>StateProvinceCode</StateProvinceCode>
               <PostalCode>PostalCode</PostalCode>
               <CountryCode>CountryCode</CountryCode>
            </Address>
            <Phone>
               <Number>Number</Number>
            </Phone>
         </ShipFrom>
         <PickupDate>PickupDate</PickupDate>
         <EarliestTimeReady>EarliestTimeReady</EarliestTimeReady>
         <LatestTimeReady>LatestTimeReady</LatestTimeReady>
         <ShipmentDetail>
            <PackagingType>
               <Code>Code</Code>
               <Description>Description</Description>
            </PackagingType>
            <NumberOfPieces>NumberOfPieces</NumberOfPieces>
            <DescriptionOfCommodity>Description</DescriptionOfCommodity>
            <Weight>
               <UnitOfMeasurement>
                  <Code>LBS</Code>
                  <Description>Pounds</Description>
               </UnitOfMeasurement>
               <Value>Value</Value>
            </Weight>
         </ShipmentDetail>
      </FreightPickupRequest>
   </tns:Body>
</tns:Envelope>
"""
