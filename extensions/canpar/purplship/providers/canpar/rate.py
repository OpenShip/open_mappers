import time
from functools import partial
from typing import List, Tuple, Optional
from canpar_lib.CanparRatingService import (
    rateShipment,
    RateShipmentRq,
    Shipment,
    Package,
    Address,
)
from purplship.core.models import (
    RateRequest,
    RateDetails,
    Message,
    ChargeDetails
)
from purplship.core.units import Packages, Services, Options
from purplship.core.utils import Serializable, Envelope, create_envelope, Element, NF, XP, DF
from purplship.providers.canpar.error import parse_error_response
from purplship.providers.canpar.utils import Settings
from purplship.providers.canpar.units import WeightUnit, DimensionUnit, Option, Service, Charges


def parse_rate_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Message]]:
    shipment_nodes = XP.find("shipment", response)
    rates: List[RateDetails] = [
        _extract_rate_details(node, settings) for node in shipment_nodes
    ]
    return rates, parse_error_response(response, settings)


def _extract_rate_details(node: Element, settings: Settings) -> RateDetails:
    shipment = XP.build(Shipment, node)
    service = Service.map(shipment.service_type)
    surcharges = [
        ChargeDetails(
            name=charge.value,
            amount=NF.decimal(getattr(shipment, charge.name)),
            currency='CAD'
        )
        for charge in list(Charges)
        if NF.decimal(getattr(shipment, charge.name)) > 0.0
    ]
    taxes = [
        ChargeDetails(
            name=f'{getattr(shipment, code)} Tax Charge',
            amount=NF.decimal(charge),
            currency='CAD'
        )
        for code, charge in [('tax_code_1', shipment.tax_charge_1), ('tax_code_2', shipment.tax_charge_2)]
        if NF.decimal(charge) > 0.0
    ]

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency="CAD",
        transit_days=shipment.transit_time,
        service=service.name_or_key,
        base_charge=NF.decimal(shipment.freight_charge),
        total_charge=sum([c.amount for c in (surcharges + taxes)], 0.0),
        duties_and_taxes=sum([t.amount for t in taxes], 0.0),
        extra_charges=(surcharges + taxes),
        meta=dict(service_name=(service.name or shipment.service_type)),
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[Envelope]:
    packages = Packages(payload.parcels)
    service_type = Services(payload.services, Service).first
    options = Options(payload.options, Option)

    shipment_date = DF.fdatetime(
        options.shipment_date or time.strftime('%Y-%m-%d'),
        current_format='%Y-%m-%d', output_format='%Y-%m-%dT%H:%M:%S'
    )
    premium: Optional[bool] = next((True for option, _ in options if option in [
        Option.canpar_ten_am.name,
        Option.canpar_noon.name,
        Option.canpar_saturday.name,
    ]), None)
    nsr = next(
        (Option[o].value for o in [
            'canpar_no_signature_required',
            'canpar_not_no_signature_required'
        ] if o in options),
        None
    )

    request = create_envelope(
        body_content=rateShipment(
            request=RateShipmentRq(
                apply_association_discount=False,
                apply_individual_discount=False,
                apply_invoice_discount=False,
                password=settings.password,
                shipment=Shipment(
                    cod_type=options['canpar_cash_on_delivery'],
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
                    dg=options['canpar_dangerous_goods'],
                    dimention_unit=DimensionUnit.IN.value,
                    handling=None,
                    handling_type=None,
                    instruction=None,
                    nsr=nsr,
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
                            xc=options['canpar_extra_care']
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
                    service_type=service_type.value,
                    shipper_num=None,
                    shipping_date=shipment_date,
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

    return Serializable(
        request, partial(
            settings.serialize,
            extra_namespace='xmlns:xsd1="http://dto.canshipws.canpar.com/xsd"',
            special_prefixes=dict(shipment_children='xsd1')
        )
    )
