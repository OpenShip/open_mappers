from typing import Tuple, List, Union
from functools import partial
from purolator_lib.pickup_service_1_2_1 import (
    SchedulePickUpResponse,
    SchedulePickUpRequest,
    RequestContext,
    Address,
    PhoneNumber,
    PickupInstruction,
    Weight,
    WeightUnit,
    NotificationEmails,
    ShipmentSummary,
    ArrayOfShipmentSummaryDetail,
    ShipmentSummaryDetail
)
from purplship.core.units import Phone, Packages
from purplship.core.models import PickupUpdateRequest, PickupRequest, PickupDetails, Message
from purplship.core.utils import (
    Serializable,
    create_envelope,
    Envelope,
    Element,
    Pipeline,
    Job,
    SF,
    XP,
)
from purplship.providers.purolator_courier.pickup.validate import validate_pickup_request
from purplship.providers.purolator_courier.error import parse_error_response
from purplship.providers.purolator_courier.utils import Settings, standard_request_serializer
from purplship.providers.purolator_courier.units import PackagePresets


def parse_pickup_response(
    response: Element, settings: Settings
) -> Tuple[PickupDetails, List[Message]]:
    reply = XP.build(
        SchedulePickUpResponse,
        next(
            iter(
                response.xpath(
                    ".//*[local-name() = $name]", name="SchedulePickUpResponse"
                )
            ),
            None,
        ),
    )
    pickup = (
        _extract_pickup_details(reply, settings)
        if reply is not None and reply.PickUpConfirmationNumber is not None
        else None
    )

    return pickup, parse_error_response(response, settings)


def _extract_pickup_details(
    reply: SchedulePickUpResponse, settings: Settings
) -> PickupDetails:

    return PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=reply.PickUpConfirmationNumber,
    )

def pickup_request(
    payload: PickupRequest, settings: Settings
) -> Serializable[Pipeline]:
    """
    Create a pickup request
    Steps
        1 - validate
        2 - create pickup
    :param payload: PickupRequest
    :param settings: Settings
    :return: Serializable[Pipeline]
    """
    request: Pipeline = Pipeline(
        validate=lambda *_: _validate_pickup(payload=payload, settings=settings),
        schedule=partial(_schedule_pickup, payload=payload, settings=settings),
    )

    return Serializable(request)


def _schedule_pickup_request(
    payload: Union[PickupRequest, PickupUpdateRequest], settings: Settings
) -> Serializable[Envelope]:
    """
    schedule_pickup_request create a serializable typed Envelope containing a SchedulePickUpRequest

    Options:
        - LoadingDockAvailable
        - TrailerAccessible

    :param payload: PickupRequest
    :param settings: Settings
    :return: Serializable[PickupRequest]
    """
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])
    phone = Phone(payload.address.phone_number, payload.address.country_code or 'CA')
    request = create_envelope(
        header_content=RequestContext(
            Version="1.2",
            Language=settings.language,
            GroupID="",
            RequestReference="",
            UserToken=settings.user_token,
        ),
        body_content=SchedulePickUpRequest(
            BillingAccountNumber=settings.account_number,
            PartnerID=None,
            PickupInstruction=PickupInstruction(
                Date=payload.pickup_date,
                AnyTimeAfter="".join(payload.ready_time.split(":")),
                UntilTime="".join(payload.closing_time.split(":")),
                TotalWeight=Weight(
                    Value=packages.weight.LB, WeightUnit=WeightUnit.LB.value
                ),
                TotalPieces=len(packages) or 1,
                BoxesIndicator=None,
                PickUpLocation=payload.package_location,
                AdditionalInstructions=payload.instruction,
                SupplyRequestCodes=None,
                TrailerAccessible=payload.options.get("TrailerAccessible"),
                LoadingDockAvailable=payload.options.get("LoadingDockAvailable"),
                ShipmentOnSkids=None,
                NumberOfSkids=None,
            ),
            Address=Address(
                Name=payload.address.person_name or "",
                Company=payload.address.company_name,
                Department=None,
                StreetNumber=payload.address.street_number,
                StreetSuffix=None,
                StreetName=payload.address.street_name,
                StreetType=payload.address.street_type,
                StreetDirection=None,
                Suite=payload.address.suite,
                Floor=None,
                StreetAddress2=SF.concat_str(payload.address.address_line2, join=True),
                StreetAddress3=None,
                City=payload.address.city,
                Province=payload.address.state_code,
                Country=payload.address.country_code,
                PostalCode=payload.address.postal_code,
                PhoneNumber=PhoneNumber(
                    CountryCode=phone.country_code or "0",
                    AreaCode=phone.area_code or "0",
                    Phone=phone.phone or "0",
                    Extension=None,
                ),
                FaxNumber=None,
            ),
            ShipmentSummary=ShipmentSummary(
                ShipmentSummaryDetails = ArrayOfShipmentSummaryDetail(
                        ShipmentSummaryDetail = [
                            ShipmentSummaryDetail(
                                DestinationCode = payload.options.get("ShipmentSummaryDetail")["DestinationCode"],
                                ModeOfTransport = payload.options.get("ShipmentSummaryDetail")["ModeOfTransport"],
                                TotalPieces = payload.options.get("ShipmentSummaryDetail")["TotalPieces"],
                                TotalWeight = Weight(
                                        Value = payload.options.get("ShipmentSummaryDetail")["WeightValue"],
                                        WeightUnit = payload.options.get("ShipmentSummaryDetail")["WeightUnit"],
                                    )
                            )
                            ]
                    )
                )
                ,
            NotificationEmails=NotificationEmails(
                NotificationEmail=[payload.address.email]
            ),
        ),
    )

    return Serializable(request, partial(standard_request_serializer, version="v1"))


def _validate_pickup(
    payload: Union[PickupRequest, PickupUpdateRequest], settings: Settings
):
    data = validate_pickup_request(payload, settings)

    return Job(id="validate", data=data)


def _schedule_pickup(
    validation_response: str, payload: PickupRequest, settings: Settings
):
    errors = parse_error_response(XP.to_xml(validation_response), settings)
    data = _schedule_pickup_request(payload, settings) if len(errors) == 0 else None

    return Job(id="schedule", data=data, fallback="")