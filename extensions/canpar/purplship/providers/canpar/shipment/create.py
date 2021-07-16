import time
from functools import partial
from typing import List, Tuple, Optional
from canpar_lib.CanshipBusinessService import (
    processShipment,
    ProcessShipmentRq,
    Shipment,
    Address,
    Package,
)
from purplship.core.models import (
    Message,
    ShipmentRequest,
    ShipmentDetails,
)
from purplship.core.utils import (
    Serializable,
    Element,
    create_envelope,
    Pipeline,
    XP,
    Job,
    DF,
)
from purplship.core.units import Packages, Options
from purplship.providers.canpar.shipment.label import get_label_request, LabelRequest
from purplship.providers.canpar.error import parse_error_response
from purplship.providers.canpar.utils import Settings
from purplship.providers.canpar.units import WeightUnit, DimensionUnit, Option, Service
from purplship.providers.canpar.rate import _extract_rate_details


def parse_shipment_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    shipment = XP.build(
        Shipment, next(iter(response.xpath(".//*[local-name() = $name]", name="shipment")), None)
    )
    success = (shipment is not None and shipment.id is not None)
    shipment_details = _extract_details(response, settings) if success else None

    return shipment_details, parse_error_response(response, settings)


def _extract_details(response: Element, settings: Settings) -> ShipmentDetails:
    shipment_node = next(iter(response.xpath(".//*[local-name() = $name]", name="shipment")), None)
    label = next(iter(response.xpath(".//*[local-name() = $name]", name="labels")), None)
    shipment = XP.build(Shipment, shipment_node)
    tracking_number = next(iter(shipment.packages), Package()).barcode

    return ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        label=str(label.text),
        tracking_number=tracking_number,
        shipment_identifier=str(shipment.id),
        selected_rate=_extract_rate_details(shipment_node, settings),
    )


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[Pipeline]:

    request: Pipeline = Pipeline(
        process=lambda *_: _process_shipment(payload, settings),
        get_label=partial(_get_label, settings=settings)
    )

    return Serializable(request)


def _process_shipment(payload: ShipmentRequest, settings: Settings) -> Job:
    packages = Packages(payload.parcels)
    options = Options(payload.options, Option)
    service_type = Service.map(payload.service).value_or_key

    premium: Optional[bool] = next((True for option, _ in options if option in [
        Option.canpar_ten_am.value,
        Option.canpar_noon.value,
        Option.canpar_saturday.value,
    ]), None)
    shipping_date = DF.fdatetime(
        options.shipment_date or time.strftime('%Y-%m-%d'),
        current_format='%Y-%m-%d', output_format='%Y-%m-%dT%H:%M:%S'
    )

    request = create_envelope(
        body_content=processShipment(
            request=ProcessShipmentRq(
                password=settings.password,
                shipment=Shipment(
                    cod_type=options.canpar_cash_on_delivery,
                    delivery_address=Address(
                        address_line_1=payload.recipient.address_line1,
                        address_line_2=payload.recipient.address_line2,
                        address_line_3=None,
                        attention=payload.recipient.person_name,
                        city=payload.recipient.city,
                        country=payload.recipient.country_code,
                        email=payload.recipient.email,
                        extension=None,
                        name=payload.recipient.company_name,
                        phone=payload.recipient.phone_number,
                        postal_code=payload.recipient.postal_code,
                        province=payload.recipient.state_code,
                        residential=payload.recipient.residential,
                    ),
                    description=None,
                    dg=options.canpar_dangerous_goods,
                    dimention_unit=DimensionUnit.IN.value,
                    handling=None,
                    handling_type=None,
                    instruction=None,
                    nsr=(options.canpar_no_signature_required or options.canpar_not_no_signature_required),
                    packages=[
                        Package(
                            alternative_reference=None,
                            cod=None,
                            cost_centre=None,
                            declared_value=None,
                            height=pkg.height.CM,
                            length=pkg.length.CM,
                            lg=None,
                            reference=None,
                            reported_weight=pkg.weight.LB,
                            store_num=None,
                            width=pkg.width.CM,
                            xc=('canpar_extra_care' in options) or None
                        ) for pkg in packages
                    ],
                    pickup_address=Address(
                        address_line_1=payload.shipper.address_line1,
                        address_line_2=payload.shipper.address_line2,
                        address_line_3=None,
                        attention=payload.shipper.person_name,
                        city=payload.shipper.city,
                        country=payload.shipper.country_code,
                        email=payload.shipper.email,
                        extension=None,
                        name=payload.shipper.company_name,
                        phone=payload.shipper.phone_number,
                        postal_code=payload.shipper.postal_code,
                        province=payload.shipper.state_code,
                        residential=payload.shipper.residential,
                    ),
                    premium=premium,
                    proforma=None,
                    reported_weight_unit=WeightUnit.LB.value,
                    send_email_to_delivery=payload.recipient.email,
                    send_email_to_pickup=payload.shipper.email,
                    service_type=service_type,
                    shipper_num=None,
                    shipping_date=shipping_date,
                    subtotal=None,
                    subtotal_with_handling=None,
                    total=None,
                    total_with_handling=None,
                    user_id=None,
                ),
                user_id=settings.username
            )
        )
    )

    data = Serializable(
        request, partial(
            settings.serialize,
            extra_namespace='xmlns:xsd1="http://dto.canshipws.canpar.com/xsd"',
            special_prefixes=dict(shipment_children='xsd1')
        )
    )
    return Job(id="process", data=data)


def _get_label(shipment_response: str, settings: Settings) -> Job:
    response = XP.to_xml(shipment_response)
    shipment = XP.build(
        Shipment, next(iter(response.xpath(".//*[local-name() = $name]", name="shipment")), None)
    )
    success = (shipment is not None and shipment.id is not None)
    data = (
        get_label_request(LabelRequest(shipment_id=shipment.id), settings)
        if success else
        None
    )

    return Job(id="get_label", data=data, fallback=("" if not success else None))
