"""Purplship Unified model definitions module."""
import attr
from typing import List, Dict, Any, Union
from jstruct import JList, JStruct, REQUIRED


@attr.s(auto_attribs=True)
class AddressExtra:
    street_name: str = None
    street_number: str = None
    street_type: str = None
    suburb: str = None
    suite: str = None


@attr.s(auto_attribs=True)
class Address:
    """shipping party (contact and address) data type."""

    id: str = None
    postal_code: str = None
    city: str = None
    person_name: str = None
    company_name: str = None
    country_code: str = None
    email: str = None
    phone_number: str = None

    state_code: str = None
    residential: bool = False

    address_line1: str = ""
    address_line2: str = ""

    street_name: str = None
    street_number: str = None
    suite: str = None
    street_type: str = None

    federal_tax_id: str = None
    state_tax_id: str = None

    extra: AddressExtra = JStruct[AddressExtra]


@attr.s(auto_attribs=True)
class Commodity:
    """commodity or product unified data type."""

    id: str = None
    sku: str = None
    quantity: int = 1
    weight: float = None
    weight_unit: str = None
    description: str = None
    value_amount: float = None
    value_currency: str = None
    origin_country: str = None


@attr.s(auto_attribs=True)
class Parcel:
    """parcel unified data type."""

    id: str = None
    weight: float = None
    width: float = None
    height: float = None
    length: float = None
    packaging_type: str = None
    package_preset: str = None
    description: str = None
    content: str = None
    is_document: bool = False
    weight_unit: str = None
    dimension_unit: str = None


@attr.s(auto_attribs=True)
class Payment:
    """payment details unified data type."""

    paid_by: str = "sender"
    currency: str = None
    account_number: str = None
    id: str = None


@attr.s(auto_attribs=True)
class Duty:
    """payment details unified data type."""

    paid_by: str = "sender"
    currency: str = None
    account_number: str = None
    declared_value: float = None
    bill_to: Address = JStruct[Address]
    id: str = None


@attr.s(auto_attribs=True)
class Customs:
    """customs info unified data type."""

    aes: str = None
    eel_pfc: str = None
    certify: bool = None
    signer: str = None
    content_type: str = None
    content_description: str = None
    incoterm: str = None
    invoice: str = None
    invoice_date: str = None
    license_number: str = None
    certificate_number: str = None
    commodities: List[Commodity] = JList[Commodity]
    duty: Duty = JStruct[Duty]
    commercial_invoice: bool = False
    options: Dict = {}
    id: str = None


@attr.s(auto_attribs=True)
class ShipmentRequest:
    """shipment request unified data type."""

    service: str

    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]

    payment: Payment = JStruct[Payment]
    customs: Customs = JStruct[Customs]

    options: Dict = {}
    reference: str = ""
    label_type: str = None


@attr.s(auto_attribs=True)
class ShipmentCancelRequest:
    """shipment cancellation request unified data type."""

    shipment_identifier: str

    service: str = None
    options: Dict = {}


@attr.s(auto_attribs=True)
class RateRequest:
    """rate fetching request unified data type."""

    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]

    services: List[str] = []
    options: Dict = {}
    reference: str = ""


@attr.s(auto_attribs=True)
class TrackingRequest:
    """tracking request unified data type."""

    tracking_numbers: List[str]
    language_code: str = None
    level_of_details: str = None


@attr.s(auto_attribs=True)
class PickupRequest:
    """pickup request unified data type."""

    pickup_date: str
    ready_time: str
    closing_time: str
    address: Address = JStruct[Address, REQUIRED]

    parcels: List[Parcel] = JList[Parcel]
    instruction: str = None
    package_location: str = None
    options: Dict = {}


@attr.s(auto_attribs=True)
class PickupUpdateRequest:
    """pickup update request unified data type."""

    confirmation_number: str
    pickup_date: str
    ready_time: str
    closing_time: str
    address: Address = JStruct[Address, REQUIRED]

    parcels: List[Parcel] = JList[Parcel]
    instruction: str = None
    package_location: str = None
    options: Dict = {}


@attr.s(auto_attribs=True)
class PickupCancelRequest:
    """pickup cancellation request unified data type."""

    confirmation_number: str

    address: Address = JStruct[Address]
    pickup_date: str = None
    reason: str = None


@attr.s(auto_attribs=True)
class AddressValidationRequest:
    """address validation request unified data type."""

    address: Address = JStruct[Address, REQUIRED]


@attr.s(auto_attribs=True)
class Message:
    """Purplship unified Message data type."""

    carrier_name: str
    carrier_id: str
    message: Union[str, Any] = None
    code: str = None
    details: Dict = None


@attr.s(auto_attribs=True)
class ChargeDetails:
    """Purplship unified charge data type."""

    name: str = None
    amount: float = None
    currency: str = None


@attr.s(auto_attribs=True)
class AddressValidationDetails:
    """Purplship unified address validation details data type."""

    carrier_name: str
    carrier_id: str
    success: bool
    complete_address: Address = None


@attr.s(auto_attribs=True)
class TrackingEvent:
    """Purplship unified tracking event data type."""

    date: str
    description: str
    location: str = None
    code: str = None
    time: str = None


@attr.s(auto_attribs=True)
class RateDetails:
    """Purplship unified rate (quote) details data type."""

    carrier_name: str
    carrier_id: str
    currency: str
    transit_days: int = None
    service: str = None
    discount: float = None
    base_charge: float = 0.0
    total_charge: float = 0.0
    duties_and_taxes: float = None
    extra_charges: List[ChargeDetails] = JList[ChargeDetails]
    meta: dict = None
    id: str = None


@attr.s(auto_attribs=True)
class TrackingDetails:
    """Purplship unified tracking details data type."""

    carrier_name: str
    carrier_id: str
    tracking_number: str
    events: List[TrackingEvent] = JList[TrackingEvent, REQUIRED]
    delivered: bool = None


@attr.s(auto_attribs=True)
class ShipmentDetails:
    """Purplship unified shipment details data type."""

    carrier_name: str
    carrier_id: str
    label: str
    tracking_number: str
    shipment_identifier: str
    selected_rate: RateDetails = JStruct[RateDetails]
    meta: dict = None
    id: str = None


@attr.s(auto_attribs=True)
class PickupDetails:
    """Purplship unified pickup details data type."""

    carrier_name: str
    carrier_id: str
    confirmation_number: str
    pickup_date: str = None
    pickup_charge: ChargeDetails = JStruct[ChargeDetails]
    ready_time: str = None
    closing_time: str = None
    id: str = None


@attr.s(auto_attribs=True)
class ConfirmationDetails:
    """Purplship unified binary operation confirmation data type."""

    carrier_name: str
    carrier_id: str
    success: bool
    operation: str
