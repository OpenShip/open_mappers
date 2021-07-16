from uuid import uuid4
from tnt_lib.shipment_request import (
    ESHIPPER,
    CONSIGNMENTBATCH,
    LOGIN,
    SENDER,
    CONSIGNMENT,
    ACTIVITY,
    CREATE,
    BOOK,
    SHIP,
    PRINT,
    LABEL,
    CONNOTE,
    MANIFEST,
    INVOICE,
    DETAILS,
    RECEIVER,
    PACKAGE,
    ARTICLE,
    RATE,
    REQUIRED,
)
from purplship.core.utils import Serializable, XP
from purplship.core.models import ShipmentRequest, Payment
from purplship.core.units import Options, Packages, Weight, WeightUnit
from purplship.providers.tnt.units import ShipmentOption, ShipmentService, PaymentType
from purplship.providers.tnt.utils import Settings


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[ESHIPPER]:
    ref = f"ref_{uuid4()}"
    options = Options(payload.options, ShipmentOption)
    package = Packages(payload.parcels).single
    service = ShipmentService.map(payload.service).value_or_key

    payment = payload.payment or Payment(paid_by='sender')
    insurance = getattr(options.tnt_insurance, 'value', None)

    request = ESHIPPER(
        LOGIN=LOGIN(
            COMPANY=settings.username,
            PASSWORD=settings.password,
            APPID='EC',
            APPVERSION=3.1,
        ),
        CONSIGNMENTBATCH=CONSIGNMENTBATCH(
            GROUPCODE=None,
            SENDER=SENDER(
                COMPANYNAME=payload.shipper.company_name,
                STREETADDRESS1=payload.shipper.address_line1,
                STREETADDRESS2=payload.shipper.address_line2,
                STREETADDRESS3=None,
                CITY=payload.shipper.city,
                PROVINCE=payload.shipper.state_code,
                POSTCODE=payload.shipper.postal_code,
                COUNTRY=payload.shipper.country_code,
                ACCOUNT=settings.account_number,
                VAT=(payload.shipper.state_tax_id or payload.shipper.federal_tax_id),
                CONTACTNAME=payload.shipper.person_name,
                CONTACTDIALCODE=None,
                CONTACTTELEPHONE=payload.shipper.phone_number,
                CONTACTEMAIL=payload.shipper.email,
                COLLECTION=None,
            ),
            CONSIGNMENT=CONSIGNMENT(
                CONREF=ref,
                DETAILS=DETAILS(
                    RECEIVER=RECEIVER(
                        COMPANYNAME=payload.recipient.company_name,
                        STREETADDRESS1=payload.recipient.address_line1,
                        STREETADDRESS2=payload.recipient.address_line2,
                        STREETADDRESS3=None,
                        CITY=payload.recipient.city,
                        PROVINCE=payload.recipient.state_code,
                        POSTCODE=payload.recipient.postal_code,
                        COUNTRY=payload.recipient.country_code,
                        VAT=(payload.recipient.state_tax_id or payload.recipient.federal_tax_id),
                        CONTACTNAME=payload.recipient.person_name,
                        CONTACTDIALCODE=None,
                        CONTACTTELEPHONE=payload.recipient.phone_number,
                        CONTACTEMAIL=payload.recipient.email,
                        ACCOUNT=None,
                        ACCOUNTCOUNTRY=None,
                    ),
                    DELIVERY=None,
                    CONNUMBER=None,
                    CUSTOMERREF=payload.reference,
                    CONTYPE=('D' if package.parcel.is_document else 'N'),
                    PAYMENTIND=PaymentType[payment.paid_by or 'sender'].value,
                    ITEMS=1,
                    TOTALWEIGHT=package.weight.KG,
                    TOTALVOLUME=package.volume,
                    CURRENCY=options.currency,
                    GOODSVALUE=insurance,
                    INSURANCEVALUE=insurance,
                    INSURANCECURRENCY=options.currency,
                    DIVISION=None,
                    SERVICE=service,
                    OPTION=[getattr(option, 'key', option) for _, option in options],
                    DESCRIPTION=package.parcel.content,
                    DELIVERYINST=None,
                    CUSTOMCONTROLIN=None,
                    HAZARDOUS=None,
                    UNNUMBER=None,
                    PACKINGGROUP=None,
                    PACKAGE=PACKAGE(
                        ITEMS=1,
                        DESCRIPTION=package.parcel.description,
                        LENGTH=package.length.M,
                        HEIGHT=package.height.M,
                        WIDTH=package.width.M,
                        WEIGHT=package.weight.KG,
                        ARTICLE=(
                            [
                                ARTICLE(
                                    ITEMS=article.quantity,
                                    DESCRIPTION=article.description,
                                    WEIGHT=Weight(article.weight, WeightUnit[article.weight_unit]).KG,
                                    INVOICEVALUE=article.value_amount,
                                    INVOICEDESC=None,
                                    HTS=article.sku,
                                    COUNTRY=article.origin_country
                                )
                                for article in payload.customs.commodities
                            ]
                            if payload.customs is not None and any(payload.customs.commodities)
                            else None
                        )
                    ),
                ),
                CONNUMBER=None,
            )
        ),
        ACTIVITY=ACTIVITY(
            CREATE=CREATE(CONREF=ref),
            RATE=RATE(CONREF=ref),
            BOOK=BOOK(CONREF=ref),
            SHIP=SHIP(CONREF=ref),
            PRINT=PRINT(
                REQUIRED=REQUIRED(CONREF=ref),
                CONNOTE=CONNOTE(CONREF=ref),
                LABEL=LABEL(CONREF=ref),
                MANIFEST=MANIFEST(CONREF=ref),
                INVOICE=INVOICE(CONREF=ref),
                EMAILTO=payload.recipient.email,
                EMAILFROM=payload.shipper.email,
            ),
            SHOW_GROUPCODE=None
        )
    )

    return Serializable(request, XP.to_xml)
