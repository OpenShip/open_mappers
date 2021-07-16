import time
from functools import reduce
from typing import List, Tuple, cast, Iterable
from dhl_express_lib.dct_req_global_2_0 import (
    DCTRequest,
    DCTTo,
    DCTFrom,
    GetQuoteType,
    BkgDetailsType,
    PiecesType,
    MetaData,
    PieceType,
    QtdShpType,
    QtdShpExChrgType,
)
from dhl_express_lib.dct_requestdatatypes_global import DCTDutiable
from dhl_express_lib.dct_response_global_2_0 import QtdShpType as ResponseQtdShpType

from purplship.core.errors import DestinationNotServicedError
from purplship.core.utils import Serializable, Element, NF, XP, DF
from purplship.core.units import Packages, Options, Package, WeightUnit, DimensionUnit, Services, CountryCurrency
from purplship.core.models import RateDetails, Message, ChargeDetails, RateRequest
from purplship.providers.dhl_express.units import (
    ProductCode,
    DCTPackageType,
    PackagePresets,
    SpecialServiceCode,
    NetworkType,
    COUNTRY_PREFERED_UNITS,
)
from purplship.providers.dhl_express.utils import Settings
from purplship.providers.dhl_express.error import parse_error_response


def parse_rate_response(
        response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    quotes = XP.find("QtdShp", response, ResponseQtdShpType)
    rates: List[RateDetails] = [
        _extract_quote(quote, settings) for quote in quotes
        if (quote.ShippingCharge is not None) or (quote.ShippingCharge is not None)
    ]

    return rates, parse_error_response(response, settings)


def _extract_quote(quote: ResponseQtdShpType, settings: Settings) -> RateDetails:
    service = ProductCode.map(quote.GlobalProductCode)
    ExtraCharges = [
        ChargeDetails(
            name=s.LocalServiceTypeName,
            amount=NF.decimal(s.ChargeValue or 0)
        )
        for s in quote.QtdShpExChrg
    ]
    discount = reduce(
        lambda d, ec: d + ec.amount if "Discount" in ec.name else d, ExtraCharges, 0.0
    )
    duties_and_taxes = reduce(
        lambda d, ec: d + ec.amount if "TAXES PAID" in ec.name else d, ExtraCharges, 0.0
    )
    delivery_date = DF.date(quote.DeliveryDate[0].DlvyDateTime, "%Y-%m-%d %H:%M:%S")
    pricing_date = DF.date(quote.PricingDate)
    transit = (
        (delivery_date.date() - pricing_date.date()).days
        if all([delivery_date, pricing_date])
        else None
    )

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=quote.CurrencyCode,
        transit_days=transit,
        service=service.name_or_key,
        base_charge=NF.decimal(quote.WeightCharge),
        total_charge=NF.decimal(quote.ShippingCharge),
        duties_and_taxes=NF.decimal(duties_and_taxes),
        discount=NF.decimal(discount),
        extra_charges=[
            ChargeDetails(
                name=s.LocalServiceTypeName,
                amount=NF.decimal(s.ChargeValue),
                currency=quote.CurrencyCode,
            )
            for s in quote.QtdShpExChrg
        ],
        meta=dict(service_name=(service.name or quote.ProductShortName))
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[DCTRequest]:
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])
    products = [*Services(payload.services, ProductCode)]
    options = Options(payload.options, SpecialServiceCode)

    is_international = payload.shipper.country_code != payload.recipient.country_code

    if not is_international and payload.shipper.country_code in ["CA"]:
        raise DestinationNotServicedError(payload.shipper.country_code)

    is_document = all([parcel.is_document for parcel in payload.parcels])
    is_dutiable = not is_document
    weight_unit, dim_unit = (COUNTRY_PREFERED_UNITS.get(payload.shipper.country_code) or packages.compatible_units)
    paperless = (SpecialServiceCode.dhl_paperless_trade if (is_international and is_dutiable) else None)
    special_services = [*options, *([(paperless.name, None)] if paperless is not None else [])]
    insurance = options['dhl_shipment_insurance'].value if 'dhl_shipment_insurance' in options else None

    if len(products) == 0:
        if is_international and is_document:
            product = 'dhl_express_worldwide_doc'
        elif is_international:
            product = 'dhl_express_worldwide_nondoc'
        elif is_document and 'envelope' in packages[0].packaging_type:
            product = 'dhl_express_envelope_doc'
        elif is_document:
            product = 'dhl_domestic_express_doc'
        else:
            product = 'dhl_express_12_00_nondoc'

        products = [ProductCode[product]]

    request = DCTRequest(
        GetQuote=GetQuoteType(
            Request=settings.Request(
                MetaData=MetaData(SoftwareName="3PV", SoftwareVersion=1.0)
            ),
            From=DCTFrom(
                CountryCode=payload.shipper.country_code,
                Postalcode=payload.shipper.postal_code,
                City=payload.shipper.city,
                Suburb=payload.shipper.state_code,
            ),
            To=DCTTo(
                CountryCode=payload.recipient.country_code,
                Postalcode=payload.recipient.postal_code,
                City=payload.recipient.city,
                Suburb=payload.recipient.state_code,
            ),
            BkgDetails=BkgDetailsType(
                PaymentCountryCode=payload.shipper.country_code,
                NetworkTypeCode=NetworkType.both_time_and_day_definite.value,
                WeightUnit=weight_unit.value,
                DimensionUnit=dim_unit.value,
                ReadyTime=time.strftime("PT%HH%MM"),
                Date=time.strftime("%Y-%m-%d"),
                IsDutiable=("Y" if is_dutiable else "N"),
                Pieces=PiecesType(
                    Piece=[
                        PieceType(
                            PieceID=package.parcel.id or f"{index}",
                            PackageTypeCode=DCTPackageType[
                                package.packaging_type or "your_packaging"
                                ].value,
                            Depth=package.length[dim_unit.name],
                            Width=package.width[dim_unit.name],
                            Height=package.height[dim_unit.name],
                            Weight=package.weight[weight_unit.name],
                        )
                        for index, package in enumerate(
                            cast(Iterable[Package], packages), 1
                        )
                    ]
                ),
                NumberOfPieces=len(packages),
                ShipmentWeight=packages.weight[weight_unit.name],
                Volume=None,
                PaymentAccountNumber=settings.account_number,
                InsuredCurrency=(options.currency if insurance is not None else None),
                InsuredValue=insurance,
                PaymentType=None,
                AcctPickupCloseTime=None,
                QtdShp=[
                    QtdShpType(
                        GlobalProductCode=product.value,
                        LocalProductCode=product.value,
                        QtdShpExChrg=[
                            QtdShpExChrgType(SpecialServiceType=SpecialServiceCode[key].value.key)
                            for key, _ in special_services if key in SpecialServiceCode
                        ],
                    )
                    for product in products
                ],
            ),
            Dutiable=(
                DCTDutiable(
                    DeclaredValue=(insurance or 1.0),
                    DeclaredCurrency=(options.currency or CountryCurrency[payload.shipper.country_code].value)
                )
                if is_dutiable else None
            ),
        ),
    )

    return Serializable(request, _request_serializer)


def _request_serializer(request: DCTRequest) -> str:
    namespacedef_ = (
        'xmlns:p="http://www.dhl.com" '
        'xmlns:p1="http://www.dhl.com/datatypes" '
        'xmlns:p2="http://www.dhl.com/DCTRequestdatatypes" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.dhl.com DCT-req.xsd "'
    )
    return XP.export(
        request,
        name_="p:DCTRequest",
        namespacedef_=namespacedef_,
    ).replace('schemaVersion="2"', 'schemaVersion="2.0"')
