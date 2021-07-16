from typing import List, Tuple
from tnt_lib.pricing_response import (
    priceResponse,
    ratedServices,
    ratedService,
    chargeElement,
)
from tnt_lib.pricing_request import (
    priceRequest,
    priceCheck,
    address,
    account,
    product,
    insurance,
    options as optionsType,
    option,
    consignmentDetails,
)
from purplship.core.utils import Serializable, Element, XP, DF, NF
from purplship.core.units import Options, Packages, Services
from purplship.core.models import RateDetails, Message, ChargeDetails, RateRequest
from purplship.providers.tnt.units import ShipmentOption, PaymentType, ShipmentService
from purplship.providers.tnt.utils import Settings
from purplship.providers.tnt.error import parse_error_response


def parse_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    price_response = XP.find("priceResponse", response, priceResponse, first=True)

    if price_response is not None and price_response.ratedServices is not None:
        rate_details = [
            _extract_detail((price_response.ratedServices, service), settings)
            for service in price_response.ratedServices.ratedService
        ]
    else:
        rate_details = []

    return rate_details, parse_error_response(response, settings)


def _extract_detail(details: Tuple[ratedServices, ratedService], settings: Settings) -> RateDetails:
    rate, service = details
    charges: List[chargeElement] = service.chargeElements.chargeElement

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        currency=rate.currency,
        service=str(service.product.id),
        base_charge=NF.decimal(service.totalPriceExclVat),
        total_charge=NF.decimal(service.totalPrice),
        duties_and_taxes=NF.decimal(service.vatAmount),
        extra_charges=[
            ChargeDetails(
                name=charge.description,
                amount=NF.decimal(charge.chargeValue),
                currency=rate.currency
            )
            for charge in charges
        ],
        meta=dict(service_name=service.product.productDesc)
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[priceRequest]:
    options = Options(payload.options, ShipmentOption)
    package = Packages(payload.parcels).single
    service = Services(payload.services, ShipmentService).first

    option_codes = [code for label, code in options if 'division' not in label]

    request = priceRequest(
        appId=settings.username,
        appVersion="3.0",
        priceCheck=priceCheck(
            rateId=None,
            sender=address(
                country=payload.shipper.country_code,
                town=payload.shipper.city,
                postcode=payload.shipper.postal_code
            ),
            delivery=address(
                country=payload.recipient.country_code,
                town=payload.recipient.city,
                postcode=payload.recipient.postal_code
            ),
            collectionDateTime=DF.fdatetime(options.shipment_date, output_format='%Y-%m-%dT%H:%M:%S'),
            product=product(
                id=getattr(service, 'value', None),
                division=next(
                    (code for label, code in options if 'division' in label),
                    None
                ),
                productDesc=None,
                type_=('D' if package.parcel.is_document else 'N'),
                options=(
                    optionsType(
                        option=[
                            option(optionCode=code)
                            for code in option_codes
                        ]
                    )
                    if any(option_codes)
                    else None
                )
            ),
            account=(
                account(
                    accountNumber=settings.account_number,
                    accountCountry=settings.account_country_code,
                )
                if any([settings.account_number, settings.account_country_code])
                else None
            ),
            insurance=(
                insurance(
                    insuranceValue=options.insurance,
                    goodsValue=options.declared_value
                )
                if options.insurance is not None
                else None
            ),
            termsOfPayment=PaymentType.sender.value,
            currency=options.currency,
            priceBreakDown=True,
            consignmentDetails=consignmentDetails(
                totalWeight=package.weight.KG,
                totalVolume=package.volume.value,
                totalNumberOfPieces=1,
            ),
            pieceLine=None
        ),
    )

    return Serializable(request, XP.to_xml)
