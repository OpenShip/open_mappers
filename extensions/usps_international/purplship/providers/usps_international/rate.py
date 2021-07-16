from typing import Tuple, List
from datetime import datetime
from usps_lib.intl_rate_v2_request import IntlRateV2Request, PackageType, ExtraServicesType, GXGType
from usps_lib.intl_rate_v2_response import ServiceType, ExtraServiceType

from purplship.core.errors import OriginNotServicedError, DestinationNotServicedError
from purplship.core.utils import Serializable, Element, NF, XP, DF
from purplship.core.models import RateDetails, Message, RateRequest, ChargeDetails
from purplship.core.units import Packages, Country, Weight, WeightUnit, Services, Options, Currency, CompleteAddress

from purplship.providers.usps_international.units import (
    ShipmentService, ShipmentOption, PackagingType, ServiceClassID
)
from purplship.providers.usps_international.error import parse_error_response
from purplship.providers.usps_international import Settings


def parse_rate_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Message]]:
    quotes: List[RateDetails] = [
        _extract_details(package, settings)
        for package in XP.find("Service", response)
    ]
    return quotes, parse_error_response(response, settings)


def _extract_details(postage_node: Element, settings: Settings) -> RateDetails:
    postage: ServiceType = XP.build(ServiceType, postage_node)

    service = ServiceClassID.map(str(postage.ID))
    charges: List[ExtraServiceType] = postage.ExtraServices.ExtraService
    delivery_date = DF.date(postage.GuaranteeAvailability, "%m/%d/%Y")
    transit = ((delivery_date.date() - datetime.now().date()).days if delivery_date is not None else None)

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        service=service.name_or_key,
        base_charge=NF.decimal(postage.Postage),
        total_charge=NF.decimal(postage.Postage),
        currency=Currency.USD.name,
        transit_days=transit,
        extra_charges=[
            ChargeDetails(
                name=charge.ServiceName,
                amount=NF.decimal(charge.Price),
                currency=Currency.USD.name,
            )
            for charge in charges
        ],
        meta=dict(service_name=service.name or postage.SvcDescription)
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[IntlRateV2Request]:
    """Create the appropriate USPS International rate request depending on the destination

    :param payload: Purplship unified API rate request data
    :param settings: USPS International connection and auth settings
    :return: a domestic or international USPS International compatible request
    :raises:
        - OriginNotServicedError when origin country is not serviced by the carrier
        - DestinationNotServicedError when destination country is US
    """

    if payload.shipper.country_code is not None and payload.shipper.country_code != Country.US.name:
        raise OriginNotServicedError(payload.shipper.country_code)

    if payload.recipient.country_code == Country.US.name:
        raise DestinationNotServicedError(payload.recipient.country_code)

    package = Packages(payload.parcels, max_weight=Weight(70, WeightUnit.LB)).single
    recipient = CompleteAddress(payload.recipient)
    options = Options(payload.options, ShipmentOption)
    services = Services(payload.services, ShipmentService)

    extra_services = [getattr(option, 'value', option) for key, option in options if 'usps_option' not in key]
    commercial = next(("Y" for svc in services if "commercial" in svc.name), "N")
    commercial_plus = next(("Y" for svc in services if "plus" in svc.name), "N")

    request = IntlRateV2Request(
        USERID=settings.username,
        Revision="2",
        Package=[
            PackageType(
                ID=0,
                Pounds=package.weight.LB,
                Ounces=package.weight.OZ,
                Machinable=options.usps_option_machinable_item or False,
                MailType=PackagingType[package.packaging_type or "package"].value,
                GXG=(
                    GXGType(POBoxFlag='N', GiftFlag='N')
                    if any('global_express_guaranteed' in s.name for s in payload.services) else None
                ),
                ValueOfContents=(options.declared_value or ""),
                Country=recipient.country_name,
                Width=package.width.IN,
                Length=package.length.IN,
                Height=package.height.IN,
                Girth=(package.girth.value if package.packaging_type == "tube" else None),
                OriginZip=payload.shipper.postal_code,
                CommercialFlag=commercial,
                CommercialPlusFlag=commercial_plus,
                AcceptanceDateTime=DF.fdatetime(
                    (options.shipment_date or datetime.today()),
                    output_format="%Y-%m-%dT%H:%M:%S"
                ),
                DestinationPostalCode=recipient.postal_code,
                ExtraServices=(
                    ExtraServicesType(ExtraService=[s for s in extra_services])
                    if any(extra_services) else None
                ),
                Content=None,
            )
        ],
    )

    return Serializable(request, XP.export)
