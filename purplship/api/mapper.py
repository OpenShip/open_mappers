"""Purplship Mapper base class definition module."""

import attr
from abc import ABC
from typing import List, Tuple
from purplship.core.settings import Settings
from purplship.core.models import (
    Message,
    RateRequest,
    TrackingRequest,
    ShipmentDetails,
    ShipmentRequest,
    VoidShipmentRequest,
    PickupRequest,
    PickupCancellationRequest,
    PickupUpdateRequest,
    PickupDetails,
    RateDetails,
    TrackingDetails,
    ConfirmationDetails,
    AddressValidationRequest,
    AddressValidationDetails
)
from purplship.core.errors import MethodNotSupportedError
from purplship.core.utils.serializable import Deserializable, Serializable


@attr.s(auto_attribs=True)
class Mapper(ABC):
    """Unified Shipping API Mapper (Interface)"""

    settings: Settings

    def create_address_validation_request(self, payload: AddressValidationRequest) -> Serializable:
        """ Create a carrier specific address validation request data from the payload """
        raise MethodNotSupportedError(
            self.__class__.create_address_validation_request.__name__, self.settings.carrier_name
        )

    def create_rate_request(self, payload: RateRequest) -> Serializable:
        """ Create a carrier specific rate request data from payload """
        raise MethodNotSupportedError(
            self.__class__.create_rate_request.__name__, self.settings.carrier_name
        )

    def parse_rate_response(
        self, response: Deserializable
    ) -> Tuple[List[RateDetails], List[Message]]:
        """ Create a unified API quote result list from carrier response  """
        raise MethodNotSupportedError(
            self.__class__.parse_rate_response.__name__, self.settings.carrier_name
        )

    def create_tracking_request(self, payload: TrackingRequest) -> Serializable:
        """ Create a carrier specific tracking request data from payload """
        raise MethodNotSupportedError(
            self.__class__.create_tracking_request.__name__, self.settings.carrier_name
        )

    def parse_tracking_response(
        self, response: Deserializable
    ) -> Tuple[List[TrackingDetails], List[Message]]:
        """ Create a unified API tracking result list from carrier response  """
        raise MethodNotSupportedError(
            self.__class__.parse_tracking_response.__name__, self.settings.carrier_name
        )

    def create_shipment_request(self, payload: ShipmentRequest) -> Serializable:
        """ Create a carrier specific shipment creation request data from payload """
        raise MethodNotSupportedError(
            self.__class__.create_shipment_request.__name__, self.settings.carrier_name
        )

    def create_void_shipment_request(self, payload: VoidShipmentRequest) -> Serializable:
        """ Create a carrier specific void shipment request data from payload """
        raise MethodNotSupportedError(
            self.__class__.create_void_shipment_request.__name__, self.settings.carrier_name
        )

    """Response Parsers"""

    def parse_address_validation_response(
        self, response: Deserializable
    ) -> Tuple[AddressValidationDetails, List[Message]]:
        """ Create a unified API address validation details from the carrier response  """
        raise MethodNotSupportedError(
            self.__class__.parse_address_validation_response.__name__, self.settings.carrier_name
        )

    def parse_shipment_response(
        self, response: Deserializable
    ) -> Tuple[ShipmentDetails, List[Message]]:
        """ Create a unified API shipment creation result from carrier response  """
        raise MethodNotSupportedError(
            self.__class__.parse_shipment_response.__name__, self.settings.carrier_name
        )

    def parse_void_shipment_response(
        self, response: Deserializable
    ) -> Tuple[ConfirmationDetails, List[Message]]:
        """ Create a unified API operation confirmation detail from the carrier response  """
        raise MethodNotSupportedError(
            self.__class__.parse_void_shipment_response.__name__, self.settings.carrier_name
        )

    def create_pickup_request(self, payload: PickupRequest) -> Serializable:
        """ Create a carrier specific pickup request xml data from payload """
        raise MethodNotSupportedError(
            self.__class__.create_pickup_request.__name__, self.settings.carrier_name
        )

    def parse_pickup_response(
        self, response: Deserializable
    ) -> Tuple[PickupDetails, List[Message]]:
        """ Create a unified API pickup result from carrier response  """
        raise MethodNotSupportedError(
            self.__class__.parse_pickup_response.__name__, self.settings.carrier_name
        )

    def create_modify_pickup_request(
        self, payload: PickupUpdateRequest
    ) -> Serializable:
        """ Create a carrier specific pickup modification request data from payload """
        raise MethodNotSupportedError(
            self.__class__.create_modify_pickup_request.__name__,
            self.settings.carrier_name,
        )

    def parse_modify_pickup_response(
        self, response: Deserializable
    ) -> Tuple[PickupDetails, List[Message]]:
        """ Create a unified API pickup result from carrier response  """
        raise MethodNotSupportedError(
            self.__class__.parse_modify_pickup_response.__name__,
            self.settings.carrier_name,
        )

    def create_cancel_pickup_request(
        self, payload: PickupCancellationRequest
    ) -> Serializable:
        """ Create a carrier specific pickup cancellation request data from payload """
        raise MethodNotSupportedError(
            self.__class__.create_cancel_pickup_request.__name__,
            self.settings.carrier_name,
        )

    def parse_cancel_pickup_response(
        self, response: Deserializable
    ) -> Tuple[ConfirmationDetails, List[Message]]:
        """ Create a united API pickup cancellation result from carrier response  """
        raise MethodNotSupportedError(
            self.__class__.parse_cancel_pickup_response.__name__,
            self.settings.carrier_name,
        )
