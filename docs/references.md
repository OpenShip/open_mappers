# References

## Standard Formats

| Type | Format
| --- | ---
| `time - str` | `HH:MM`
| `date - str` | `YYYY-MM-DD`
| `datetime - str` | `YYYY-MM-DD HH:MM`

## WEIGHT UNITS

| Code | Identifier
| --- | ---
| `KG` | KG
| `LB` | LB


## DIMENSION UNITS

| Code | Identifier
| --- | ---
| `CM` | CM
| `IN` | IN

---


## Gateway


#### Aramex Settings `[carrier_name = aramex]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `account_pin` | `str` | **required**
| `account_entity` | `str` | **required**
| `account_number` | `str` | **required**
| `account_country_code` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Australia Post Settings `[carrier_name = australiapost]`

| Name | Type | Description 
| --- | --- | --- |
| `api_key` | `str` | **required**
| `password` | `str` | **required**
| `account_number` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Canada Post Settings `[carrier_name = canadapost]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `customer_number` | `str` | **required**
| `contract_id` | `str` | 
| `language` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Canpar Settings `[carrier_name = canpar]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### DHL Express Settings `[carrier_name = dhl_express]`

| Name | Type | Description 
| --- | --- | --- |
| `site_id` | `str` | **required**
| `password` | `str` | **required**
| `account_number` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### DHL Universal Settings `[carrier_name = dhl_universal]`

| Name | Type | Description 
| --- | --- | --- |
| `consumer_key` | `str` | **required**
| `consumer_secret` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Dicom Settings `[carrier_name = dicom]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `billing_account` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### FedEx Settings `[carrier_name = fedex]`

| Name | Type | Description 
| --- | --- | --- |
| `user_key` | `str` | **required**
| `password` | `str` | **required**
| `meter_number` | `str` | **required**
| `account_number` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Purolator Settings `[carrier_name = purolator]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `account_number` | `str` | **required**
| `language` | `str` | 
| `user_token` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Royal Mail Settings `[carrier_name = royalmail]`

| Name | Type | Description 
| --- | --- | --- |
| `client_id` | `str` | **required**
| `client_secret` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Sendle Settings `[carrier_name = sendle]`

| Name | Type | Description 
| --- | --- | --- |
| `sendle_id` | `str` | **required**
| `api_key` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### SF-Express Settings `[carrier_name = sf_express]`

| Name | Type | Description 
| --- | --- | --- |
| `partner_id` | `str` | **required**
| `check_word` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### TNT Settings `[carrier_name = tnt]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `account_number` | `str` | 
| `account_country_code` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### UPS Settings `[carrier_name = ups]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `access_license_number` | `str` | **required**
| `account_number` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### USPS Settings `[carrier_name = usps]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `mailer_id` | `str` | 
| `customer_registration_id` | `str` | 
| `logistics_manager_mailer_id` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### USPS International Settings `[carrier_name = usps_international]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `mailer_id` | `str` | 
| `customer_registration_id` | `str` | 
| `logistics_manager_mailer_id` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Yanwen Settings `[carrier_name = yanwen]`

| Name | Type | Description 
| --- | --- | --- |
| `customer_number` | `str` | **required**
| `license_key` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Yunexpress Settings `[carrier_name = yunexpress]`

| Name | Type | Description 
| --- | --- | --- |
| `customer_number` | `str` | **required**
| `api_secret` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


*Note that all carrier gateway defined above have these additional parameters*

| Name | Type | Description
| --- | --- | --- |
| `carrier_name` | `str` | readonly: carrier name (eg: canadapost, purolator...)


---


## Models

All models can be imported at `from purplship.core.models import [ModelName]`

#### Address

| Name | Type | Description 
| --- | --- | --- |
| `id` | `str` | 
| `postal_code` | `str` | 
| `city` | `str` | 
| `person_name` | `str` | 
| `company_name` | `str` | 
| `country_code` | `str` | 
| `email` | `str` | 
| `phone_number` | `str` | 
| `state_code` | `str` | 
| `residential` | `bool` | 
| `address_line1` | `str` | 
| `address_line2` | `str` | 
| `federal_tax_id` | `str` | 
| `state_tax_id` | `str` | 
| `extra` | [AddressExtra](#addressextra) | 


#### AddressExtra

| Name | Type | Description 
| --- | --- | --- |
| `street_name` | `str` | 
| `street_number` | `str` | 
| `street_type` | `str` | 
| `suburb` | `str` | 
| `suite` | `str` | 


#### AddressValidationDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `success` | `bool` | **required**
| `complete_address` | [Address](#address) | 


#### AddressValidationRequest

| Name | Type | Description 
| --- | --- | --- |
| `address` | [Address](#address) | **required**


#### ChargeDetails

| Name | Type | Description 
| --- | --- | --- |
| `name` | `str` | 
| `amount` | `float` | 
| `currency` | `str` | 


#### Commodity

| Name | Type | Description 
| --- | --- | --- |
| `id` | `str` | 
| `sku` | `str` | 
| `quantity` | `int` | 
| `weight` | `float` | 
| `weight_unit` | `str` | 
| `description` | `str` | 
| `value_amount` | `float` | 
| `value_currency` | `str` | 
| `origin_country` | `str` | 


#### ConfirmationDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `success` | `bool` | **required**
| `operation` | `str` | **required**


#### Customs

| Name | Type | Description 
| --- | --- | --- |
| `aes` | `str` | 
| `eel_pfc` | `str` | 
| `certify` | `bool` | 
| `signer` | `str` | 
| `content_type` | `str` | 
| `content_description` | `str` | 
| `incoterm` | `str` | 
| `invoice` | `str` | 
| `invoice_date` | `str` | 
| `license_number` | `str` | 
| `certificate_number` | `str` | 
| `commodities` | List[[Commodity](#commodity)] | 
| `duty` | [Duty](#duty) | 
| `commercial_invoice` | `bool` | 
| `options` | `dict` | 
| `id` | `str` | 


#### Duty

| Name | Type | Description 
| --- | --- | --- |
| `paid_by` | `str` | 
| `currency` | `str` | 
| `account_number` | `str` | 
| `declared_value` | `float` | 
| `bill_to` | [Address](#address) | 
| `id` | `str` | 


#### Message

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `message` | Union[str, Any] | 
| `code` | `str` | 
| `details` | `dict` | 


#### Parcel

| Name | Type | Description 
| --- | --- | --- |
| `id` | `str` | 
| `weight` | `float` | 
| `width` | `float` | 
| `height` | `float` | 
| `length` | `float` | 
| `packaging_type` | `str` | 
| `package_preset` | `str` | 
| `description` | `str` | 
| `content` | `str` | 
| `is_document` | `bool` | 
| `weight_unit` | `str` | 
| `dimension_unit` | `str` | 


#### Payment

| Name | Type | Description 
| --- | --- | --- |
| `paid_by` | `str` | 
| `currency` | `str` | 
| `account_number` | `str` | 
| `id` | `str` | 


#### PickupCancelRequest

| Name | Type | Description 
| --- | --- | --- |
| `confirmation_number` | `str` | **required**
| `address` | [Address](#address) | 
| `pickup_date` | `str` | 
| `reason` | `str` | 


#### PickupDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `confirmation_number` | `str` | **required**
| `pickup_date` | `str` | 
| `pickup_charge` | [ChargeDetails](#chargedetails) | 
| `ready_time` | `str` | 
| `closing_time` | `str` | 
| `id` | `str` | 


#### PickupRequest

| Name | Type | Description 
| --- | --- | --- |
| `pickup_date` | `str` | **required**
| `ready_time` | `str` | **required**
| `closing_time` | `str` | **required**
| `address` | [Address](#address) | **required**
| `parcels` | List[[Parcel](#parcel)] | 
| `instruction` | `str` | 
| `package_location` | `str` | 
| `options` | `dict` | 


#### PickupUpdateRequest

| Name | Type | Description 
| --- | --- | --- |
| `confirmation_number` | `str` | **required**
| `pickup_date` | `str` | **required**
| `ready_time` | `str` | **required**
| `closing_time` | `str` | **required**
| `address` | [Address](#address) | **required**
| `parcels` | List[[Parcel](#parcel)] | 
| `instruction` | `str` | 
| `package_location` | `str` | 
| `options` | `dict` | 


#### RateDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `currency` | `str` | **required**
| `transit_days` | `int` | 
| `service` | `str` | 
| `discount` | `float` | 
| `base_charge` | `float` | 
| `total_charge` | `float` | 
| `duties_and_taxes` | `float` | 
| `extra_charges` | List[[ChargeDetails](#chargedetails)] | 
| `meta` | `dict` | 
| `id` | `str` | 


#### RateRequest

| Name | Type | Description 
| --- | --- | --- |
| `shipper` | [Address](#address) | **required**
| `recipient` | [Address](#address) | **required**
| `parcels` | List[[Parcel](#parcel)] | **required**
| `services` | List[str] | 
| `options` | `dict` | 
| `reference` | `str` | 


#### ShipmentCancelRequest

| Name | Type | Description 
| --- | --- | --- |
| `shipment_identifier` | `str` | **required**
| `service` | `str` | 
| `options` | `dict` | 


#### ShipmentDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `label` | `str` | **required**
| `tracking_number` | `str` | **required**
| `shipment_identifier` | `str` | **required**
| `selected_rate` | [RateDetails](#ratedetails) | 
| `meta` | `dict` | 
| `id` | `str` | 


#### ShipmentRequest

| Name | Type | Description 
| --- | --- | --- |
| `service` | `str` | **required**
| `shipper` | [Address](#address) | **required**
| `recipient` | [Address](#address) | **required**
| `parcels` | List[[Parcel](#parcel)] | **required**
| `payment` | [Payment](#payment) | 
| `customs` | [Customs](#customs) | 
| `options` | `dict` | 
| `reference` | `str` | 
| `label_type` | `str` | 


#### TrackingDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `tracking_number` | `str` | **required**
| `events` | List[[TrackingEvent](#trackingevent)] | **required**
| `delivered` | `bool` | 


#### TrackingEvent

| Name | Type | Description 
| --- | --- | --- |
| `date` | `str` | **required**
| `description` | `str` | **required**
| `location` | `str` | 
| `code` | `str` | 
| `time` | `str` | 


#### TrackingRequest

| Name | Type | Description 
| --- | --- | --- |
| `tracking_numbers` | List[str] | **required**
| `language_code` | `str` | 
| `level_of_details` | `str` | 

---


## Packaging Types


#### Multi-carrier (purplship)

| Code | Identifier
| --- | ---
| `envelope` | Small Envelope
| `pak` | Pak
| `tube` | Tube
| `pallet` | Pallet
| `small_box` | Small Box
| `medium_box` | Medium Box
| `your_packaging` | Your Packaging


#### DHL Express

| Code | Identifier
| --- | ---
| `dhl_flyer_smalls` | FLY
| `dhl_parcels_conveyables` | COY
| `dhl_non_conveyables` | NCY
| `dhl_pallets` | PAL
| `dhl_double_pallets` | DBL
| `dhl_box` | BOX


#### FedEx

| Code | Identifier
| --- | ---
| `fedex_envelope` | FEDEX_ENVELOPE
| `fedex_pak` | FEDEX_PAK
| `fedex_box` | FEDEX_BOX
| `fedex_10_kg_box` | FEDEX_10KG_BOX
| `fedex_25_kg_box` | FEDEX_25KG_BOX
| `fedex_tube` | FEDEX_TUBE
| `your_packaging` | YOUR_PACKAGING


#### Purolator

| Code | Identifier
| --- | ---
| `purolator_express_envelope` | Envelope
| `purolator_express_pack` | Pack
| `purolator_express_box` | Box
| `purolator_customer_packaging` | Customer Packaging


#### TNT

| Code | Identifier
| --- | ---
| `tnt_envelope` | envelope
| `tnt_satchel` | satchel
| `tnt_box` | box
| `tnt_cylinder` | cylinder
| `tnt_pallet` | pallet
| `your_packaging` | your_packaging


#### UPS

| Code | Identifier
| --- | ---
| `ups_unknown` | 00
| `ups_letter` | 01
| `ups_package` | 02
| `ups_tube` | 03
| `ups_pak` | 04
| `ups_express_box` | 21
| `ups_box_25_kg` | 24
| `ups_box_10_kg` | 25
| `ups_pallet` | 30
| `ups_small_express_box` | 2a
| `ups_medium_express_box` | 2b
| `ups_large_express_box` | 2c

---


## Package Presets


#### Canada Post

| Code | Dimensions | Note
| --- | --- | ---
| `canadapost_mailing_box` | 15.2 x 1.0 x 10.2 | height x length x width
| `canadapost_extra_small_mailing_box` | 14.0 x 14.0 x 14.0 | height x length x width
| `canadapost_small_mailing_box` | 22.9 x 6.4 x 28.6 | height x length x width
| `canadapost_medium_mailing_box` | 23.5 x 13.3 x 31.0 | height x length x width
| `canadapost_large_mailing_box` | 30.5 x 9.5 x 38.1 | height x length x width
| `canadapost_extra_large_mailing_box` | 30.5 x 21.6 x 40.0 | height x length x width
| `canadapost_corrugated_small_box` | 32.0 x 32.0 x 42.0 | height x length x width
| `canadapost_corrugated_medium_box` | 38.0 x 32.0 x 46.0 | height x length x width
| `canadapost_corrugated_large_box` | 46.0 x 40.6 x 46.0 | height x length x width
| `canadapost_xexpresspost_certified_envelope` | 15.9 x 1.5 x 0.5 x 26.0 | height x length x weight x width
| `canadapost_xexpresspost_national_large_envelope` | 29.2 x 1.5 x 1.36 x 40.0 | height x length x weight x width


#### DHL Express

| Code | Dimensions | Note
| --- | --- | ---
| `dhl_express_envelope` | 27.5 x 1.0 x 0.5 x 35.0 | height x length x weight x width
| `dhl_express_standard_flyer` | 30.0 x 1.5 x 2.0 x 40.0 | height x length x weight x width
| `dhl_express_large_flyer` | 37.5 x 1.5 x 3.0 x 47.5 | height x length x weight x width
| `dhl_express_box_2` | 18.2 x 10.0 x 1.0 x 33.7 | height x length x weight x width
| `dhl_express_box_3` | 32.0 x 5.2 x 2.0 x 33.6 | height x length x weight x width
| `dhl_express_box_4` | 32.2 x 18.0 x 5.0 x 33.7 | height x length x weight x width
| `dhl_express_box_5` | 32.2 x 34.5 x 10.0 x 33.7 | height x length x weight x width
| `dhl_express_box_6` | 35.9 x 36.9 x 15.0 x 41.7 | height x length x weight x width
| `dhl_express_box_7` | 40.4 x 38.9 x 20.0 x 48.1 | height x length x weight x width
| `dhl_express_box_8` | 44.4 x 40.9 x 25.0 x 54.2 | height x length x weight x width
| `dhl_express_tube` | 15.0 x 15.0 x 5.0 x 96.0 | height x length x weight x width
| `dhl_didgeridoo_box` | 13.0 x 162.0 x 10.0 x 13.0 | height x length x weight x width
| `dhl_jumbo_box` | 42.7 x 33.0 x 30.0 x 45.0 | height x length x weight x width
| `dhl_jumbo_box_junior` | 34.0 x 24.1 x 20.0 x 39.9 | height x length x weight x width


#### FedEx

| Code | Dimensions | Note
| --- | --- | ---
| `fedex_envelope_legal_size` | 15.5 x 1.0 x 9.5 | height x weight x width
| `fedex_padded_pak` | 14.75 x 2.2 x 11.75 | height x weight x width
| `fedex_polyethylene_pak` | 15.5 x 2.2 x 12.0 | height x weight x width
| `fedex_clinical_pak` | 18.0 x 2.2 x 13.5 | height x weight x width
| `fedex_small_box` | 10.9 x 1.5 x 20.0 x 12.25 | height x length x weight x width
| `fedex_medium_box` | 11.5 x 2.38 x 20.0 x 13.25 | height x length x weight x width
| `fedex_large_box` | 12.38 x 3.0 x 20.0 x 17.88 | height x length x weight x width
| `fedex_10_kg_box` | 12.94 x 10.19 x 10.0 x 15.81 | height x length x weight x width
| `fedex_25_kg_box` | 16.56 x 13.19 x 25.0 x 21.56 | height x length x weight x width
| `fedex_tube` | 6.0 x 6.0 x 20.0 x 38.0 | height x length x weight x width


#### Purolator

| Code | Dimensions | Note
| --- | --- | ---
| `purolator_express_envelope` | 1.5 x 1.0 x 12.5 | length x weight x width
| `purolator_express_pack` | 1.0 x 3.0 x 12.5 | length x weight x width
| `purolator_express_box` | 3.5 x 7.0 | length x weight


#### TNT

| Code | Dimensions | Note
| --- | --- | ---
| `tnt_envelope_doc` | 1.0 x 27.5 x 35.0 | height x length x width
| `tnt_satchel_bag1` | 1.0 x 30.0 x 2.0 x 40.0 | height x length x weight x width
| `tnt_satchel_bag2` | 1.0 x 38.0 x 4.0 x 47.5 | height x length x weight x width
| `tnt_box_B` | 19.0 x 40.0 x 4.0 x 29.5 | height x length x weight x width
| `tnt_box_C` | 29.0 x 40.0 x 6.0 x 29.5 | height x length x weight x width
| `tnt_box_D` | 29.0 x 50.0 x 10.0 x 39.5 | height x length x weight x width
| `tnt_box_E` | 49.5 x 44.0 x 15.0 x 39.5 | height x length x weight x width
| `tnt_medpack_ambient` | 12.0 x 23.0 x 18.0 | height x length x width
| `tnt_medpack_fronzen_10` | 35.5 x 40.0 x 37.0 | height x length x width


#### UPS

| Code | Dimensions | Note
| --- | --- | ---
| `ups_small_express_box` | 11.0 x 2.0 x 30.0 x 13.0 | height x length x weight x width
| `ups_medium_express_box` | 11.0 x 3.0 x 30.0 x 16.0 | height x length x weight x width
| `ups_large_express_box` | 13.0 x 3.0 x 30.0 x 18.0 | height x length x weight x width
| `ups_express_tube` | 6.0 x 6.0 x 38.0 | height x length x width
| `ups_express_pak` | 11.75 x 1.5 x 16.0 | height x length x width
| `ups_world_document_box` | 12.5 x 3.0 x 17.5 | height x length x width

---


## Shipping Services


#### Canada Post

| Code | Identifier
| --- | ---
| `canadapost_regular_parcel` | DOM.RP
| `canadapost_expedited_parcel` | DOM.EP
| `canadapost_xpresspost` | DOM.XP
| `canadapost_priority` | DOM.PC
| `canadapost_library_books` | DOM.LIB
| `canadapost_expedited_parcel_usa` | USA.EP
| `canadapost_priority_worldwide_envelope_usa` | USA.PW.ENV
| `canadapost_priority_worldwide_pak_usa` | USA.PW.PAK
| `canadapost_priority_worldwide_parcel_usa` | USA.PW.PARCEL
| `canadapost_small_packet_usa_air` | USA.SP.AIR
| `canadapost_tracked_packet_usa` | USA.TP
| `canadapost_tracked_packet_usa_lvm` | USA.TP.LVM
| `canadapost_xpresspost_usa` | USA.XP
| `canadapost_xpresspost_international` | INT.XP
| `canadapost_international_parcel_air` | INT.IP.AIR
| `canadapost_international_parcel_surface` | INT.IP.SURF
| `canadapost_priority_worldwide_envelope_intl` | INT.PW.ENV
| `canadapost_priority_worldwide_pak_intl` | INT.PW.PAK
| `canadapost_priority_worldwide_parcel_intl` | INT.PW.PARCEL
| `canadapost_small_packet_international_air` | INT.SP.AIR
| `canadapost_small_packet_international_surface` | INT.SP.SURF
| `canadapost_tracked_packet_international` | INT.TP


#### DHL Express

| Code | Identifier
| --- | ---
| `dhl_logistics_services` | 0
| `dhl_domestic_express_12_00_doc` | 1
| `dhl_b2_c_doc` | 2
| `dhl_b2_c_nondoc` | 3
| `dhl_jetline` | 4
| `dhl_sprintline` | 5
| `dhl_express_easy_doc` | 7
| `dhl_express_easy_nondoc` | 8
| `dhl_europack_doc` | 9
| `dhl_auto_reversals` | A
| `dhl_breakbulk_express_doc` | B
| `dhl_medical_express_doc` | C
| `dhl_express_worldwide_doc` | D
| `dhl_express_9_00_nondoc` | E
| `dhl_freight_worldwide_nondoc` | F
| `dhl_domestic_economy_select_doc` | G
| `dhl_economy_select_nondoc` | H
| `dhl_domestic_express_9_00_doc` | I
| `dhl_jumbo_box_nondoc` | J
| `dhl_express_9_00_doc` | K
| `dhl_express_10_30_doc` | L
| `dhl_express_10_30_nondoc` | M
| `dhl_domestic_express_doc` | N
| `dhl_domestic_express_10_30_doc` | O
| `dhl_express_worldwide_nondoc` | P
| `dhl_medical_express_nondoc` | Q
| `dhl_globalmail_business_doc` | R
| `dhl_same_day_doc` | S
| `dhl_express_12_00_doc` | T
| `dhl_express_worldwide_ecx_doc` | U
| `dhl_europack_nondoc` | V
| `dhl_economy_select_doc` | W
| `dhl_express_envelope_doc` | X
| `dhl_express_12_00_nondoc` | Y
| `dhl_destination_charges` | Z


#### FedEx

| Code | Identifier
| --- | ---
| `fedex_europe_first_international_priority` | EUROPE_FIRST_INTERNATIONAL_PRIORITY
| `fedex_1_day_freight` | FEDEX_1_DAY_FREIGHT
| `fedex_2_day` | FEDEX_2_DAY
| `fedex_2_day_am` | FEDEX_2_DAY_AM
| `fedex_2_day_freight` | FEDEX_2_DAY_FREIGHT
| `fedex_3_day_freight` | FEDEX_3_DAY_FREIGHT
| `fedex_cargo_airport_to_airport` | FEDEX_CARGO_AIRPORT_TO_AIRPORT
| `fedex_cargo_freight_forwarding` | FEDEX_CARGO_FREIGHT_FORWARDING
| `fedex_cargo_international_express_freight` | FEDEX_CARGO_INTERNATIONAL_EXPRESS_FREIGHT
| `fedex_cargo_international_premium` | FEDEX_CARGO_INTERNATIONAL_PREMIUM
| `fedex_cargo_mail` | FEDEX_CARGO_MAIL
| `fedex_cargo_registered_mail` | FEDEX_CARGO_REGISTERED_MAIL
| `fedex_cargo_surface_mail` | FEDEX_CARGO_SURFACE_MAIL
| `fedex_custom_critical_air_expedite` | FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE
| `fedex_custom_critical_air_expedite_exclusive_use` | FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE_EXCLUSIVE_USE
| `fedex_custom_critical_air_expedite_network` | FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE_NETWORK
| `fedex_custom_critical_charter_air` | FEDEX_CUSTOM_CRITICAL_CHARTER_AIR
| `fedex_custom_critical_point_to_point` | FEDEX_CUSTOM_CRITICAL_POINT_TO_POINT
| `fedex_custom_critical_surface_expedite` | FEDEX_CUSTOM_CRITICAL_SURFACE_EXPEDITE
| `fedex_custom_critical_surface_expedite_exclusive_use` | FEDEX_CUSTOM_CRITICAL_SURFACE_EXPEDITE_EXCLUSIVE_USE
| `fedex_custom_critical_temp_assure_air` | FEDEX_CUSTOM_CRITICAL_TEMP_ASSURE_AIR
| `fedex_custom_critical_temp_assure_validated_air` | FEDEX_CUSTOM_CRITICAL_TEMP_ASSURE_VALIDATED_AIR
| `fedex_custom_critical_white_glove_services` | FEDEX_CUSTOM_CRITICAL_WHITE_GLOVE_SERVICES
| `fedex_distance_deferred` | FEDEX_DISTANCE_DEFERRED
| `fedex_express_saver` | FEDEX_EXPRESS_SAVER
| `fedex_first_freight` | FEDEX_FIRST_FREIGHT
| `fedex_freight_economy` | FEDEX_FREIGHT_ECONOMY
| `fedex_freight_priority` | FEDEX_FREIGHT_PRIORITY
| `fedex_ground` | FEDEX_GROUND
| `fedex_international_priority_plus` | FEDEX_INTERNATIONAL_PRIORITY_PLUS
| `fedex_next_day_afternoon` | FEDEX_NEXT_DAY_AFTERNOON
| `fedex_next_day_early_morning` | FEDEX_NEXT_DAY_EARLY_MORNING
| `fedex_next_day_end_of_day` | FEDEX_NEXT_DAY_END_OF_DAY
| `fedex_next_day_freight` | FEDEX_NEXT_DAY_FREIGHT
| `fedex_next_day_mid_morning` | FEDEX_NEXT_DAY_MID_MORNING
| `fedex_first_overnight` | FIRST_OVERNIGHT
| `fedex_ground_home_delivery` | GROUND_HOME_DELIVERY
| `fedex_international_distribution_freight` | INTERNATIONAL_DISTRIBUTION_FREIGHT
| `fedex_international_economy` | INTERNATIONAL_ECONOMY
| `fedex_international_economy_distribution` | INTERNATIONAL_ECONOMY_DISTRIBUTION
| `fedex_international_economy_freight` | INTERNATIONAL_ECONOMY_FREIGHT
| `fedex_international_first` | INTERNATIONAL_FIRST
| `fedex_international_ground` | INTERNATIONAL_GROUND
| `fedex_international_priority` | INTERNATIONAL_PRIORITY
| `fedex_international_priority_distribution` | INTERNATIONAL_PRIORITY_DISTRIBUTION
| `fedex_international_priority_express` | INTERNATIONAL_PRIORITY_EXPRESS
| `fedex_international_priority_freight` | INTERNATIONAL_PRIORITY_FREIGHT
| `fedex_priority_overnight` | PRIORITY_OVERNIGHT
| `fedex_same_day` | SAME_DAY
| `fedex_same_day_city` | SAME_DAY_CITY
| `fedex_same_day_metro_afternoon` | SAME_DAY_METRO_AFTERNOON
| `fedex_same_day_metro_morning` | SAME_DAY_METRO_MORNING
| `fedex_same_day_metro_rush` | SAME_DAY_METRO_RUSH
| `fedex_smart_post` | SMART_POST
| `fedex_standard_overnight` | STANDARD_OVERNIGHT
| `fedex_transborder_distribution_consolidation` | TRANSBORDER_DISTRIBUTION_CONSOLIDATION


#### Purolator

| Code | Identifier
| --- | ---
| `purolator_express_9_am` | PurolatorExpress9AM
| `purolator_express_us` | PurolatorExpressU.S.
| `purolator_express_10_30_am` | PurolatorExpress10:30AM
| `purolator_express_us_9_am` | PurolatorExpressU.S.9AM
| `purolator_express_12_pm` | PurolatorExpress12PM
| `purolator_express_us_10_30_am` | PurolatorExpressU.S.10:30AM
| `purolator_express` | PurolatorExpress
| `purolator_express_us_12_00` | PurolatorExpressU.S.12:00
| `purolator_express_evening` | PurolatorExpressEvening
| `purolator_express_envelope_us` | PurolatorExpressEnvelopeU.S.
| `purolator_express_envelope_9_am` | PurolatorExpressEnvelope9AM
| `purolator_express_us_envelope_9_am` | PurolatorExpressU.S.Envelope9AM
| `purolator_express_envelope_10_30_am` | PurolatorExpressEnvelope10:30AM
| `purolator_express_us_envelope_10_30_am` | PurolatorExpressU.S.Envelope10:30AM
| `purolator_express_envelope_12_pm` | PurolatorExpressEnvelope12PM
| `purolator_express_us_envelope_12_00` | PurolatorExpressU.S.Envelope12:00
| `purolator_express_envelope` | PurolatorExpressEnvelope
| `purolator_express_pack_us` | PurolatorExpressPackU.S.
| `purolator_express_envelope_evening` | PurolatorExpressEnvelopeEvening
| `purolator_express_us_pack_9_am` | PurolatorExpressU.S.Pack9AM
| `purolator_express_pack_9_am` | PurolatorExpressPack9AM
| `purolator_express_us_pack_10_30_am` | PurolatorExpressU.S.Pack10:30AM
| `purolator_express_pack10_30_am` | PurolatorExpressPack10:30AM
| `purolator_express_us_pack_12_00` | PurolatorExpressU.S.Pack12:00
| `purolator_express_pack_12_pm` | PurolatorExpressPack12PM
| `purolator_express_box_us` | PurolatorExpressBoxU.S.
| `purolator_express_pack` | PurolatorExpressPack
| `purolator_express_us_box_9_am` | PurolatorExpressU.S.Box9AM
| `purolator_express_pack_evening` | PurolatorExpressPackEvening
| `purolator_express_us_box_10_30_am` | PurolatorExpressU.S.Box10:30AM
| `purolator_express_box_9_am` | PurolatorExpressBox9AM
| `purolator_express_us_box_12_00` | PurolatorExpressU.S.Box12:00
| `purolator_express_box_10_30_am` | PurolatorExpressBox10:30AM
| `purolator_ground_us` | PurolatorGroundU.S.
| `purolator_express_box_12_pm` | PurolatorExpressBox12PM
| `purolator_express_international` | PurolatorExpressInternational
| `purolator_express_box` | PurolatorExpressBox
| `purolator_express_international_9_am` | PurolatorExpressInternational9AM
| `purolator_express_box_evening` | PurolatorExpressBoxEvening
| `purolator_express_international_10_30_am` | PurolatorExpressInternational10:30AM
| `purolator_ground` | PurolatorGround
| `purolator_express_international_12_00` | PurolatorExpressInternational12:00
| `purolator_ground9_am` | PurolatorGround9AM
| `purolator_express_envelope_international` | PurolatorExpressEnvelopeInternational
| `purolator_ground10_30_am` | PurolatorGround10:30AM
| `purolator_express_international_envelope_9_am` | PurolatorExpressInternationalEnvelope9AM
| `purolator_ground_evening` | PurolatorGroundEvening
| `purolator_express_international_envelope_10_30_am` | PurolatorExpressInternationalEnvelope10:30AM
| `purolator_quick_ship` | PurolatorQuickShip
| `purolator_express_international_envelope_12_00` | PurolatorExpressInternationalEnvelope12:00
| `purolator_quick_ship_envelope` | PurolatorQuickShipEnvelope
| `purolator_express_pack_international` | PurolatorExpressPackInternational
| `purolator_quick_ship_pack` | PurolatorQuickShipPack
| `purolator_express_international_pack_9_am` | PurolatorExpressInternationalPack9AM
| `purolator_quick_ship_box` | PurolatorQuickShipBox
| `purolator_express_international_pack_10_30_am` | PurolatorExpressInternationalPack10:30AM
| `purolator_express_international_pack_12_00` | PurolatorExpressInternationalPack12:00
| `purolator_express_box_international` | PurolatorExpressBoxInternational
| `purolator_express_international_box_9_am` | PurolatorExpressInternationalBox9AM
| `purolator_express_international_box_10_30_am` | PurolatorExpressInternationalBox10:30AM
| `purolator_express_international_box_12_00` | PurolatorExpressInternationalBox12:00


#### TNT

| Code | Identifier
| --- | ---
| `tnt_special_express` | 1N
| `tnt_9_00_express` | 09N
| `tnt_10_00_express` | 10N
| `tnt_12_00_express` | 12N
| `tnt_express` | EX
| `tnt_economy_express` | 48N
| `tnt_global_express` | 15N


#### UPS

| Code | Identifier
| --- | ---
| `ups_standard` | 11
| `ups_worldwide_expedited` | 08
| `ups_worldwide_express` | 07
| `ups_worldwide_express_plus` | 54
| `ups_worldwide_saver` | 65
| `ups_2nd_day_air` | 02
| `ups_2nd_day_air_am` | 59
| `ups_3_day_select` | 12
| `ups_expedited_mail_innovations` | M4
| `ups_first_class_mail` | M2
| `ups_ground` | 03
| `ups_next_day_air` | 01
| `ups_next_day_air_early` | 14
| `ups_next_day_air_saver` | 13
| `ups_priority_mail` | M3
| `ups_access_point_economy` | 70
| `ups_today_dedicated_courier` | 83
| `ups_today_express` | 85
| `ups_today_express_saver` | 86
| `ups_today_standard` | 82
| `ups_worldwide_express_freight` | 96
| `ups_priority_mail_innovations` | M5
| `ups_economy_mail_innovations` | M6


#### USPS

| Code | Identifier
| --- | ---
| `usps_first_class` | First Class
| `usps_first_class_commercial` | First Class Commercial
| `usps_first_class_hfp_commercial` | First Class HFPCommercial
| `usps_priority` | Priority
| `usps_priority_commercial` | Priority Commercial
| `usps_priority_cpp` | Priority Cpp
| `usps_priority_hfp_commercial` | Priority HFP Commercial
| `usps_priority_hfp_cpp` | Priority HFP CPP
| `usps_priority_mail_express` | Priority Mail Express
| `usps_priority_mail_express_commercial` | Priority Mail Express Commercial
| `usps_priority_mail_express_cpp` | Priority Mail Express CPP
| `usps_priority_mail_express_sh` | Priority Mail Express Sh
| `usps_priority_mail_express_sh_commercial` | Priority Mail Express ShCommercial
| `usps_priority_mail_express_hfp` | Priority Mail Express HFP
| `usps_priority_mail_express_hfp_commercial` | Priority Mail Express HFP Commercial
| `usps_priority_mail_express_hfp_cpp` | Priority Mail Express HFP CPP
| `usps_priority_mail_cubic` | Priority Mail Cubic
| `usps_retail_ground` | Retail Ground
| `usps_media` | Media
| `usps_library` | Library
| `usps_all` | All
| `usps_online` | Online
| `usps_plus` | Plus
| `usps_bpm` | BPM


#### USPS International

| Code | Identifier
| --- | ---
| `usps_first_class` | First Class
| `usps_first_class_commercial` | First Class Commercial
| `usps_first_class_hfp_commercial` | First Class HFPCommercial
| `usps_priority` | Priority
| `usps_priority_commercial` | Priority Commercial
| `usps_priority_cpp` | Priority Cpp
| `usps_priority_hfp_commercial` | Priority HFP Commercial
| `usps_priority_hfp_cpp` | Priority HFP CPP
| `usps_priority_mail_express` | Priority Mail Express
| `usps_priority_mail_express_commercial` | Priority Mail Express Commercial
| `usps_priority_mail_express_cpp` | Priority Mail Express CPP
| `usps_priority_mail_express_sh` | Priority Mail Express Sh
| `usps_priority_mail_express_sh_commercial` | Priority Mail Express ShCommercial
| `usps_priority_mail_express_hfp` | Priority Mail Express HFP
| `usps_priority_mail_express_hfp_commercial` | Priority Mail Express HFP Commercial
| `usps_priority_mail_express_hfp_cpp` | Priority Mail Express HFP CPP
| `usps_priority_mail_cubic` | Priority Mail Cubic
| `usps_retail_ground` | Retail Ground
| `usps_media` | Media
| `usps_library` | Library
| `usps_all` | All
| `usps_online` | Online
| `usps_plus` | Plus
| `usps_bpm` | BPM

---


## Shipping Options


#### Multi-carrier (purplship)

| Code | Identifier | Description
| --- | --- | ---
| `currency` | currency | `str`
| `insurance` | insurance | `float`
| `cash_on_delivery` | COD | `float`
| `label_format` | label_format | `str`
| `shipment_date` | shipment_date | `str`
| `label_printing` | label_printing | `str`
| `declared_value` | declared_value | `float`
| `notification_emails` | notification_emails | `str`
| `signature_confirmation` | signature_confirmation | `bool`


#### Canada Post

| Code | Identifier | Description
| --- | --- | ---
| `canadapost_signature` | SO | `bool`
| `canadapost_coverage` | COV | `float`
| `canadapost_collect_on_delivery` | COD | `float`
| `canadapost_proof_of_age_required_18` | PA18 | `bool`
| `canadapost_proof_of_age_required_19` | PA19 | `bool`
| `canadapost_card_for_pickup` | HFP | `bool`
| `canadapost_do_not_safe_drop` | DNS | `bool`
| `canadapost_leave_at_door` | LAD | `bool`
| `canadapost_deliver_to_post_office` | D2PO | `bool`
| `canadapost_return_at_senders_expense` | RASE | `bool`
| `canadapost_return_to_sender` | RTS | `bool`
| `canadapost_abandon` | ABAN | `bool`


#### DHL Express

| Code | Identifier | Description
| --- | --- | ---
| `dhl_logistics_services` | 0A | `bool`
| `dhl_mailroom_management` | 0B | `bool`
| `dhl_pallet_administration` | 0C | `bool`
| `dhl_warehousing` | 0D | `bool`
| `dhl_express_logistics_centre` | 0E | `bool`
| `dhl_strategic_parts_centre` | 0F | `bool`
| `dhl_local_distribution_centre` | 0G | `bool`
| `dhl_terminal_handling` | 0H | `bool`
| `dhl_cross_docking` | 0I | `bool`
| `dhl_inventory_management` | 0J | `bool`
| `dhl_loading_unloading` | 0K | `bool`
| `dhl_product_kitting` | 0L | `bool`
| `dhl_priority_account_desk` | 0M | `bool`
| `dhl_document_archiving` | 0N | `bool`
| `dhl_saturday_delivery` | AA | `bool`
| `dhl_saturday_pickup` | AB | `bool`
| `dhl_holiday_delivery` | AC | `bool`
| `dhl_holiday_pickup` | AD | `bool`
| `dhl_domestic_saturday_delivery` | AG | `bool`
| `dhl_standard` | BA | `bool`
| `dhl_globalmail_item` | BB | `bool`
| `dhl_letter` | BC | `bool`
| `dhl_packet` | BD | `bool`
| `dhl_letter_plus` | BE | `bool`
| `dhl_packet_plus` | BF | `bool`
| `dhl_elevated_risk` | CA | `bool`
| `dhl_restricted_destination` | CB | `bool`
| `dhl_security_validation` | CC | `bool`
| `dhl_secure_protection` | CD | `bool`
| `dhl_proof_of_identity` | CE | `bool`
| `dhl_secure_storage` | CF | `bool`
| `dhl_diplomatic_material` | CG | `bool`
| `dhl_smart_sensor` | CH | `bool`
| `dhl_visa_program` | CI | `bool`
| `dhl_onboard_courier` | CJ | `bool`
| `dhl_secure_safebox` | CK | `bool`
| `dhl_smart_sentry` | CL | `bool`
| `dhl_split_duties_and_tax` | DC | `bool`
| `dhl_duties_and_taxes_paid` | DD | `bool`
| `dhl_receiver_paid` | DE | `bool`
| `dhl_duties_and_taxes_unpaid` | DS | `bool`
| `dhl_import_billing` | DT | `bool`
| `dhl_importer_of_record` | DU | `bool`
| `dhl_go_green_carbon_neutral` | EA | `bool`
| `dhl_go_green_carbon_footprint` | EB | `bool`
| `dhl_go_green_carbon_estimate` | EC | `bool`
| `dhl_fuel_surcharge_b` | FB | `bool`
| `dhl_fuel_surcharge_c` | FC | `bool`
| `dhl_fuel_surcharge_f` | FF | `bool`
| `dhl_smartphone_box` | GA | `bool`
| `dhl_laptop_box` | GB | `bool`
| `dhl_bottle_box` | GC | `bool`
| `dhl_repacking` | GD | `bool`
| `dhl_tablet_box` | GE | `bool`
| `dhl_filler_material` | GF | `bool`
| `dhl_packaging` | GG | `bool`
| `dhl_diplomatic_bag` | GH | `bool`
| `dhl_pallet_box` | GI | `bool`
| `dhl_lock_box` | GJ | `bool`
| `dhl_lithium_ion_pi965_section_ii` | HB | `bool`
| `dhl_dry_ice_un1845` | HC | `bool`
| `dhl_lithium_ion_pi965_966_section_ii` | HD | `bool`
| `dhl_dangerous_goods` | HE | `bool`
| `dhl_perishable_cargo` | HG | `bool`
| `dhl_excepted_quantity` | HH | `bool`
| `dhl_spill_cleaning` | HI | `bool`
| `dhl_consumer_commodities` | HK | `bool`
| `dhl_limited_quantities_adr` | HL | `bool`
| `dhl_lithium_metal_pi969_section_ii` | HM | `bool`
| `dhl_adr_load_exemption` | HN | `bool`
| `dhl_lithium_ion_pi967_section_ii` | HV | `bool`
| `dhl_lithium_metal_pi970_section_ii` | HW | `bool`
| `dhl_biological_un3373` | HY | `bool`
| `dhl_extended_liability` | IB | `bool`
| `dhl_contract_insurance` | IC | `bool`
| `dhl_shipment_insurance` | II | `float`
| `dhl_delivery_notification` | JA | `str`
| `dhl_pickup_notification` | JC | `bool`
| `dhl_proactive_tracking` | JD | `bool`
| `dhl_performance_reporting` | JE | `bool`
| `dhl_prealert_notification` | JY | `bool`
| `dhl_change_of_billing` | KA | `bool`
| `dhl_cash_on_delivery` | KB | `float`
| `dhl_printed_invoice` | KD | `bool`
| `dhl_waybill_copy` | KE | `bool`
| `dhl_import_paperwork` | KF | `bool`
| `dhl_payment_on_pickup` | KY | `bool`
| `dhl_shipment_intercept` | LA | `bool`
| `dhl_shipment_redirect` | LC | `bool`
| `dhl_storage_at_facility` | LE | `bool`
| `dhl_cold_storage` | LG | `bool`
| `dhl_specific_routing` | LH | `bool`
| `dhl_service_recovery` | LV | `bool`
| `dhl_alternative_address` | LW | `bool`
| `dhl_hold_for_collection` | LX | `bool`
| `dhl_address_correction_a` | MA | `bool`
| `dhl_address_correction_b` | MB | `bool`
| `dhl_neutral_delivery` | NN | `bool`
| `dhl_remote_area_pickup` | OB | `bool`
| `dhl_remote_area_delivery_c` | OC | `bool`
| `dhl_out_of_service_area` | OE | `bool`
| `dhl_remote_area_delivery_o` | OO | `bool`
| `dhl_shipment_preparation` | PA | `bool`
| `dhl_shipment_labeling` | PB | `bool`
| `dhl_shipment_consolidation` | PC | `bool`
| `dhl_relabeling_data_entry` | PD | `bool`
| `dhl_preprinted_waybill` | PE | `bool`
| `dhl_piece_labelling` | PS | `bool`
| `dhl_data_staging_03` | PT | `bool`
| `dhl_data_staging_06` | PU | `bool`
| `dhl_data_staging_12` | PV | `bool`
| `dhl_data_staging_24` | PW | `bool`
| `dhl_standard_pickup` | PX | `bool`
| `dhl_scheduled_pickup` | PY | `bool`
| `dhl_dedicated_pickup` | QA | `bool`
| `dhl_early_pickup` | QB | `bool`
| `dhl_late_pickup` | QD | `bool`
| `dhl_residential_pickup` | QE | `bool`
| `dhl_loading_waiting` | QF | `bool`
| `dhl_bypass_injection` | QH | `bool`
| `dhl_direct_injection` | QI | `bool`
| `dhl_drop_off_at_facility` | QY | `bool`
| `dhl_delivery_signature` | SA | `bool`
| `dhl_content_signature` | SB | `bool`
| `dhl_named_signature` | SC | `bool`
| `dhl_adult_signature` | SD | `bool`
| `dhl_contract_signature` | SE | `bool`
| `dhl_alternative_signature` | SW | `bool`
| `dhl_no_signature_required` | SX | `bool`
| `dhl_dedicated_delivery` | TA | `bool`
| `dhl_early_delivery` | TB | `bool`
| `dhl_time_window_delivery` | TC | `bool`
| `dhl_evening_delivery` | TD | `bool`
| `dhl_delivery_on_appointment` | TE | `bool`
| `dhl_return_undeliverable` | TG | `bool`
| `dhl_swap_delivery` | TH | `bool`
| `dhl_unloading_waiting` | TJ | `bool`
| `dhl_residential_delivery` | TK | `bool`
| `dhl_repeat_delivery` | TN | `bool`
| `dhl_alternative_date` | TT | `bool`
| `dhl_no_partial_delivery` | TU | `bool`
| `dhl_service_point_24_7` | TV | `bool`
| `dhl_pre_9_00` | TW | `bool`
| `dhl_pre_10_30` | TX | `bool`
| `dhl_pre_12_00` | TY | `bool`
| `dhl_thermo_packaging` | UA | `bool`
| `dhl_ambient_vialsafe` | UB | `bool`
| `dhl_ambient_non_insulated` | UC | `bool`
| `dhl_ambient_insulated` | UD | `bool`
| `dhl_ambient_extreme` | UE | `bool`
| `dhl_chilled_box_s` | UF | `bool`
| `dhl_chilled_box_m` | UG | `bool`
| `dhl_chilled_box_l` | UH | `bool`
| `dhl_frozen_no_ice_s` | UI | `bool`
| `dhl_frozen_no_ice_m` | UJ | `bool`
| `dhl_frozen_no_ice_l` | UK | `bool`
| `dhl_frozen_ice_sticks_s` | UL | `bool`
| `dhl_frozen_ice_sticks_m` | UM | `bool`
| `dhl_frozen_ice_sticks_l` | UN | `bool`
| `dhl_frozen_ice_plates_s` | UO | `bool`
| `dhl_frozen_ice_plates_m` | UP | `bool`
| `dhl_frozen_ice_plates_l` | UQ | `bool`
| `dhl_combination_no_ice` | UR | `bool`
| `dhl_combination_dry_ice` | US | `bool`
| `dhl_frozen_ice_sticks_e` | UT | `bool`
| `dhl_frozen_ice_plates_e` | UV | `bool`
| `dhl_customer_tcp_1` | UW | `bool`
| `dhl_thermo_accessories` | VA | `bool`
| `dhl_absorbent_sleeve` | VB | `bool`
| `dhl_cooland_wrap` | VC | `bool`
| `dhl_dry_ice_supplies` | VD | `bool`
| `dhl_pressure_bag_s` | VE | `bool`
| `dhl_pressure_bag_m` | VF | `bool`
| `dhl_pressure_bag_l` | VG | `bool`
| `dhl_informal_clearance` | WA | `bool`
| `dhl_formal_clearance` | WB | `bool`
| `dhl_payment_deferment` | WC | `bool`
| `dhl_clearance_authorization` | WD | `bool`
| `dhl_multiline_entry` | WE | `bool`
| `dhl_post_clearance_modification` | WF | `bool`
| `dhl_handover_to_broker` | WG | `bool`
| `dhl_physical_intervention` | WH | `bool`
| `dhl_bio_phyto_veterinary_controls` | WI | `bool`
| `dhl_obtaining_permits_and_licences` | WJ | `bool`
| `dhl_bonded_storage` | WK | `bool`
| `dhl_bonded_transit_documents` | WL | `bool`
| `dhl_temporary_import_export` | WM | `bool`
| `dhl_under_bond_guarantee` | WN | `bool`
| `dhl_export_declaration` | WO | `bool`
| `dhl_exporter_validation` | WP | `bool`
| `dhl_certificate_of_origin` | WQ | `bool`
| `dhl_document_translation` | WR | `bool`
| `dhl_personal_effects` | WS | `bool`
| `dhl_paperless_trade` | WY | `bool`
| `dhl_import_export_taxes` | XB | `bool`
| `dhl_unrecoverable_origin_tax` | XC | `bool`
| `dhl_quarantine_inspection` | XD | `bool`
| `dhl_merchandise_process` | XE | `bool`
| `dhl_domestic_postal_tax` | XF | `bool`
| `dhl_tier_two_tax` | XG | `bool`
| `dhl_tier_three_tax` | XH | `bool`
| `dhl_import_penalty` | XI | `bool`
| `dhl_cargo_zone_process` | XJ | `bool`
| `dhl_import_export_duties` | XX | `bool`
| `dhl_premium_09_00` | Y1 | `bool`
| `dhl_premium_10_30` | Y2 | `bool`
| `dhl_premium_12_00` | Y3 | `bool`
| `dhl_over_sized_piece_b` | YB | `bool`
| `dhl_over_handled_piece_c` | YC | `bool`
| `dhl_multipiece_shipment` | YE | `bool`
| `dhl_over_weight_piece_f` | YF | `bool`
| `dhl_over_sized_piece_g` | YG | `bool`
| `dhl_over_handled_piece_h` | YH | `bool`
| `dhl_premium_9_00_i` | YI | `bool`
| `dhl_premium_10_30_j` | YJ | `bool`
| `dhl_premium_12_00_k` | YK | `bool`
| `dhl_paket_shipment` | YV | `bool`
| `dhl_breakbulk_mother` | YW | `bool`
| `dhl_breakbulk_baby` | YX | `bool`
| `dhl_over_weight_piece_y` | YY | `bool`
| `dhl_customer_claim` | ZA | `bool`
| `dhl_damage_compensation` | ZB | `bool`
| `dhl_loss_compensation` | ZC | `bool`
| `dhl_customer_rebate` | ZD | `bool`
| `dhl_e_com_discount` | ZE | `bool`


#### FedEx

| Code | Identifier | Description
| --- | --- | ---
| `fedex_blind_shipment` | BLIND_SHIPMENT | `bool`
| `fedex_broker_select_option` | BROKER_SELECT_OPTION | `bool`
| `fedex_call_before_delivery` | CALL_BEFORE_DELIVERY | `bool`
| `fedex_cod` | COD | `str`
| `fedex_cod_remittance` | COD_REMITTANCE | `bool`
| `fedex_custom_delivery_window` | CUSTOM_DELIVERY_WINDOW | `bool`
| `fedex_cut_flowers` | CUT_FLOWERS | `bool`
| `fedex_dangerous_goods` | DANGEROUS_GOODS | `bool`
| `fedex_delivery_on_invoice_acceptance` | DELIVERY_ON_INVOICE_ACCEPTANCE | `bool`
| `fedex_detention` | DETENTION | `bool`
| `fedex_do_not_break_down_pallets` | DO_NOT_BREAK_DOWN_PALLETS | `bool`
| `fedex_do_not_stack_pallets` | DO_NOT_STACK_PALLETS | `bool`
| `fedex_dry_ice` | DRY_ICE | `bool`
| `fedex_east_coast_special` | EAST_COAST_SPECIAL | `bool`
| `fedex_electronic_trade_documents` | ELECTRONIC_TRADE_DOCUMENTS | `bool`
| `fedex_event_notification` | EVENT_NOTIFICATION | `bool`
| `fedex_exclude_from_consolidation` | EXCLUDE_FROM_CONSOLIDATION | `bool`
| `fedex_exclusive_use` | EXCLUSIVE_USE | `bool`
| `fedex_exhibition_delivery` | EXHIBITION_DELIVERY | `bool`
| `fedex_exhibition_pickup` | EXHIBITION_PICKUP | `bool`
| `fedex_expedited_alternate_delivery_route` | EXPEDITED_ALTERNATE_DELIVERY_ROUTE | `bool`
| `fedex_expedited_one_day_earlier` | EXPEDITED_ONE_DAY_EARLIER | `bool`
| `fedex_expedited_service_monitoring_and_delivery` | EXPEDITED_SERVICE_MONITORING_AND_DELIVERY | `bool`
| `fedex_expedited_standard_day_early_delivery` | EXPEDITED_STANDARD_DAY_EARLY_DELIVERY | `bool`
| `fedex_extra_labor` | EXTRA_LABOR | `bool`
| `fedex_extreme_length` | EXTREME_LENGTH | `bool`
| `fedex_one_rate` | FEDEX_ONE_RATE | `bool`
| `fedex_flatbed_trailer` | FLATBED_TRAILER | `bool`
| `fedex_food` | FOOD | `bool`
| `fedex_freight_guarantee` | FREIGHT_GUARANTEE | `bool`
| `fedex_freight_to_collect` | FREIGHT_TO_COLLECT | `bool`
| `fedex_future_day_shipment` | FUTURE_DAY_SHIPMENT | `bool`
| `fedex_hold_at_location` | HOLD_AT_LOCATION | `bool`
| `fedex_holiday_delivery` | HOLIDAY_DELIVERY | `bool`
| `fedex_holiday_guarantee` | HOLIDAY_GUARANTEE | `bool`
| `fedex_home_delivery_premium` | HOME_DELIVERY_PREMIUM | `bool`
| `fedex_inside_delivery` | INSIDE_DELIVERY | `bool`
| `fedex_inside_pickup` | INSIDE_PICKUP | `bool`
| `fedex_international_controlled_export_service` | INTERNATIONAL_CONTROLLED_EXPORT_SERVICE | `bool`
| `fedex_international_mail_service` | INTERNATIONAL_MAIL_SERVICE | `bool`
| `fedex_international_traffic_in_arms_regulations` | INTERNATIONAL_TRAFFIC_IN_ARMS_REGULATIONS | `bool`
| `fedex_liftgate_delivery` | LIFTGATE_DELIVERY | `bool`
| `fedex_liftgate_pickup` | LIFTGATE_PICKUP | `bool`
| `fedex_limited_access_delivery` | LIMITED_ACCESS_DELIVERY | `bool`
| `fedex_limited_access_pickup` | LIMITED_ACCESS_PICKUP | `bool`
| `fedex_marking_or_tagging` | MARKING_OR_TAGGING | `bool`
| `fedex_non_business_time` | NON_BUSINESS_TIME | `bool`
| `fedex_pallet_shrinkwrap` | PALLET_SHRINKWRAP | `bool`
| `fedex_pallet_weight_allowance` | PALLET_WEIGHT_ALLOWANCE | `bool`
| `fedex_pallets_provided` | PALLETS_PROVIDED | `bool`
| `fedex_pending_complete` | PENDING_COMPLETE | `bool`
| `fedex_pending_shipment` | PENDING_SHIPMENT | `bool`
| `fedex_permit` | PERMIT | `bool`
| `fedex_pharmacy_delivery` | PHARMACY_DELIVERY | `bool`
| `fedex_poison` | POISON | `bool`
| `fedex_port_delivery` | PORT_DELIVERY | `bool`
| `fedex_port_pickup` | PORT_PICKUP | `bool`
| `fedex_pre_delivery_notification` | PRE_DELIVERY_NOTIFICATION | `bool`
| `fedex_pre_eig_processing` | PRE_EIG_PROCESSING | `bool`
| `fedex_pre_multiplier_processing` | PRE_MULTIPLIER_PROCESSING | `bool`
| `fedex_protection_from_freezing` | PROTECTION_FROM_FREEZING | `bool`
| `fedex_regional_mall_delivery` | REGIONAL_MALL_DELIVERY | `bool`
| `fedex_regional_mall_pickup` | REGIONAL_MALL_PICKUP | `bool`
| `fedex_return_shipment` | RETURN_SHIPMENT | `bool`
| `fedex_returns_clearance` | RETURNS_CLEARANCE | `bool`
| `fedex_returns_clearance_special_routing_required` | RETURNS_CLEARANCE_SPECIAL_ROUTING_REQUIRED | `bool`
| `fedex_saturday_delivery` | SATURDAY_DELIVERY | `bool`
| `fedex_saturday_pickup` | SATURDAY_PICKUP | `bool`
| `fedex_shipment_assembly` | SHIPMENT_ASSEMBLY | `bool`
| `fedex_sort_and_segregate` | SORT_AND_SEGREGATE | `bool`
| `fedex_special_delivery` | SPECIAL_DELIVERY | `bool`
| `fedex_special_equipment` | SPECIAL_EQUIPMENT | `bool`
| `fedex_storage` | STORAGE | `bool`
| `fedex_sunday_delivery` | SUNDAY_DELIVERY | `bool`
| `fedex_third_party_consignee` | THIRD_PARTY_CONSIGNEE | `bool`
| `fedex_top_load` | TOP_LOAD | `bool`
| `fedex_usps_delivery` | USPS_DELIVERY | `bool`
| `fedex_usps_pickup` | USPS_PICKUP | `bool`
| `fedex_weighing` | WEIGHING | `bool`


#### Purolator

| Code | Identifier | Description
| --- | --- | ---
| `purolator_dangerous_goods` | Dangerous Goods | `bool`
| `purolator_chain_of_signature` | Chain of Signature | `bool`
| `purolator_express_cheque` | ExpressCheque | `bool`
| `purolator_hold_for_pickup` | Hold For Pickup | `bool`
| `purolator_return_services` | Return Services | `bool`
| `purolator_saturday_service` | Saturday Service | `bool`
| `purolator_origin_signature_not_required` | Origin Signature Not Required (OSNR) | `bool`
| `purolator_adult_signature_required` | Adult Signature Required (ASR) | `bool`
| `purolator_special_handling` | Special Handling | `bool`
| `purolator_show_alternative_services` | Show Alternate Services | `bool`


#### TNT

| Code | Identifier | Description
| --- | --- | ---
| `tnt_priority` | PR | `bool`
| `tnt_insurance` | IN | `float`
| `tnt_enhanced_liability` | EL | `bool`
| `tnt_dangerous_goods_fully_regulated` | HZ | `bool`
| `tnt_dangerous_goods_in_limited_quantities` | LQ | `bool`
| `tnt_dry_ice_shipments` | DI | `bool`
| `tnt_biological_substances` | BB | `bool`
| `tnt_lithium_batteries` | LB | `bool`
| `tnt_dangerous_goods_in_excepted_quantities` | EQ | `bool`
| `tnt_radioactive_materials_in_excepted_packages` | XP | `bool`
| `tnt_pre_delivery_notification` | SMS | `bool`
| `tnt_division_international_shipments` | G | `bool`
| `tnt_division_global_link_domestic` | D | `bool`
| `tnt_division_german_domestic` | H | `bool`
| `tnt_division_uk_domestic` | 010 | `bool`


#### UPS

| Code | Identifier | Description
| --- | --- | ---
| `ups_saturday_delivery_indicator` | SaturdayDeliveryIndicator | `bool`
| `ups_access_point_cod` | AccessPointCOD | `float`
| `ups_deliver_to_addressee_only_indicator` | DeliverToAddresseeOnlyIndicator | `bool`
| `ups_direct_delivery_only_indicator` | DirectDeliveryOnlyIndicator | `bool`
| `ups_cod` | COD | `float`
| `ups_delivery_confirmation` | DeliveryConfirmation | `bool`
| `ups_return_of_document_indicator` | ReturnOfDocumentIndicator | `bool`
| `ups_carbonneutral_indicator` | UPScarbonneutralIndicator | `bool`
| `ups_certificate_of_origin_indicator` | CertificateOfOriginIndicator | `bool`
| `ups_pickup_options` | PickupOptions | `bool`
| `ups_delivery_options` | DeliveryOptions | `bool`
| `ups_restricted_articles` | RestrictedArticles | `bool`
| `ups_shipper_export_declaration_indicator` | ShipperExportDeclarationIndicator | `bool`
| `ups_commercial_invoice_removal_indicator` | CommercialInvoiceRemovalIndicator | `bool`
| `ups_import_control` | ImportControl | `bool`
| `ups_return_service` | ReturnService | `bool`
| `ups_sdl_shipment_indicator` | SDLShipmentIndicator | `bool`
| `ups_epra_indicator` | EPRAIndicator | `bool`


#### USPS

| Code | Identifier | Description
| --- | --- | ---
| `usps_insurance` | 100 | `float`
| `usps_insurance_priority_mail_express` | 101 | `float`
| `usps_return_receipt` | 102 | `bool`
| `usps_collect_on_delivery` | 103 | `bool`
| `usps_certificate_of_mailing_form_3665` | 104 | `bool`
| `usps_certified_mail` | 105 | `bool`
| `usps_tracking` | 106 | `bool`
| `usps_signature_confirmation` | 108 | `bool`
| `usps_registered_mail` | 109 | `bool`
| `usps_return_receipt_electronic` | 110 | `bool`
| `usps_registered_mail_cod_collection_charge` | 112 | `bool`
| `usps_return_receipt_priority_mail_express` | 118 | `bool`
| `usps_adult_signature_required` | 119 | `bool`
| `usps_adult_signature_restricted_delivery` | 120 | `bool`
| `usps_insurance_priority_mail` | 125 | `float`
| `usps_tracking_electronic` | 155 | `bool`
| `usps_signature_confirmation_electronic` | 156 | `bool`
| `usps_certificate_of_mailing_form_3817` | 160 | `bool`
| `usps_priority_mail_express_10_30_am_delivery` | 161 | `bool`
| `usps_certified_mail_restricted_delivery` | 170 | `bool`
| `usps_certified_mail_adult_signature_required` | 171 | `bool`
| `usps_certified_mail_adult_signature_restricted_delivery` | 172 | `bool`
| `usps_signature_confirm_restrict_delivery` | 173 | `bool`
| `usps_signature_confirmation_electronic_restricted_delivery` | 174 | `bool`
| `usps_collect_on_delivery_restricted_delivery` | 175 | `bool`
| `usps_registered_mail_restricted_delivery` | 176 | `bool`
| `usps_insurance_restricted_delivery` | 177 | `float`
| `usps_insurance_restrict_delivery_priority_mail` | 179 | `float`
| `usps_insurance_restrict_delivery_priority_mail_express` | 178 | `float`
| `usps_insurance_restrict_delivery_bulk_only` | 180 | `float`
| `usps_scan_retention` | 181 | `bool`
| `usps_scan_signature_retention` | 182 | `bool`
| `usps_special_handling_fragile` | 190 | `bool`
| `usps_option_machinable_item` | usps_option_machinable_item | `bool`
| `usps_option_ground_only` | usps_option_ground_only | `bool`
| `usps_option_return_service_info` | usps_option_return_service_info | `bool`
| `usps_option_ship_info` | usps_option_ship_info | `bool`


#### USPS International

| Code | Identifier | Description
| --- | --- | ---
| `usps_registered_mail` | 103 | `bool`
| `usps_insurance_global_express_guaranteed` | 106 | `bool`
| `usps_insurance_express_mail_international` | 107 | `bool`
| `usps_insurance_priority_mail_international` | 108 | `bool`
| `usps_return_receipt` | 105 | `bool`
| `usps_certificate_of_mailing` | 100 | `bool`
| `usps_electronic_usps_delivery_confirmation_international` | 109 | `bool`
| `usps_option_machinable_item` | usps_option_machinable_item | `bool`
| `usps_option_abandon_non_delivery` | ABANDON | `bool`
| `usps_option_return_non_delivery` | RETURN | `bool`
| `usps_option_redirect_non_delivery` | REDIRECT | Address


---


## Countries

| Code | Name
| --- | ---
| `AD` | Andorra
| `AE` | United Arab Emirates
| `AF` | Afghanistan
| `AG` | Antigua
| `AI` | Anguilla
| `AL` | Albania
| `AM` | Armenia
| `AN` | Netherlands Antilles
| `AO` | Angola
| `AR` | Argentina
| `AS` | American Samoa
| `AT` | Austria
| `AU` | Australia
| `AW` | Aruba
| `AZ` | Azerbaijan
| `BA` | Bosnia And Herzegovina
| `BB` | Barbados
| `BD` | Bangladesh
| `BE` | Belgium
| `BF` | Burkina Faso
| `BG` | Bulgaria
| `BH` | Bahrain
| `BI` | Burundi
| `BJ` | Benin
| `BM` | Bermuda
| `BN` | Brunei
| `BO` | Bolivia
| `BR` | Brazil
| `BS` | Bahamas
| `BT` | Bhutan
| `BW` | Botswana
| `BY` | Belarus
| `BZ` | Belize
| `CA` | Canada
| `CD` | Congo, The Democratic Republic Of
| `CF` | Central African Republic
| `CG` | Congo
| `CH` | Switzerland
| `CI` | Cote D Ivoire
| `CK` | Cook Islands
| `CL` | Chile
| `CM` | Cameroon
| `CN` | China, Peoples Republic
| `CO` | Colombia
| `CR` | Costa Rica
| `CU` | Cuba
| `CV` | Cape Verde
| `CY` | Cyprus
| `CZ` | Czech Republic, The
| `DE` | Germany
| `DJ` | Djibouti
| `DK` | Denmark
| `DM` | Dominica
| `DO` | Dominican Republic
| `DZ` | Algeria
| `EC` | Ecuador
| `EE` | Estonia
| `EG` | Egypt
| `ER` | Eritrea
| `ES` | Spain
| `ET` | Ethiopia
| `FI` | Finland
| `FJ` | Fiji
| `FK` | Falkland Islands
| `FM` | Micronesia, Federated States Of
| `FO` | Faroe Islands
| `FR` | France
| `GA` | Gabon
| `GB` | United Kingdom
| `GD` | Grenada
| `GE` | Georgia
| `GF` | French Guyana
| `GG` | Guernsey
| `GH` | Ghana
| `GI` | Gibraltar
| `GL` | Greenland
| `GM` | Gambia
| `GN` | Guinea Republic
| `GP` | Guadeloupe
| `GQ` | Guinea-equatorial
| `GR` | Greece
| `GT` | Guatemala
| `GU` | Guam
| `GW` | Guinea-bissau
| `GY` | Guyana (british)
| `HK` | Hong Kong
| `HN` | Honduras
| `HR` | Croatia
| `HT` | Haiti
| `HU` | Hungary
| `IC` | Canary Islands, The
| `ID` | Indonesia
| `IE` | Ireland, Republic Of
| `IL` | Israel
| `IN` | India
| `IQ` | Iraq
| `IR` | Iran (islamic Republic Of)
| `IS` | Iceland
| `IT` | Italy
| `JE` | Jersey
| `JM` | Jamaica
| `JO` | Jordan
| `JP` | Japan
| `KE` | Kenya
| `KG` | Kyrgyzstan
| `KH` | Cambodia
| `KI` | Kiribati
| `KM` | Comoros
| `KN` | St. Kitts
| `KP` | Korea, The D.p.r Of (north K.)
| `KR` | Korea, Republic Of (south K.)
| `KV` | Kosovo
| `KW` | Kuwait
| `KY` | Cayman Islands
| `KZ` | Kazakhstan
| `LA` | Lao Peoples Democratic Republic
| `LB` | Lebanon
| `LC` | St. Lucia
| `LI` | Liechtenstein
| `LK` | Sri Lanka
| `LR` | Liberia
| `LS` | Lesotho
| `LT` | Lithuania
| `LU` | Luxembourg
| `LV` | Latvia
| `LY` | Libya
| `MA` | Morocco
| `MC` | Monaco
| `MD` | Moldova, Republic Of
| `ME` | Montenegro, Republic Of
| `MG` | Madagascar
| `MH` | Marshall Islands
| `MK` | Macedonia, Republic Of
| `ML` | Mali
| `MM` | Myanmar
| `MN` | Mongolia
| `MO` | Macau
| `MP` | Commonwealth No. Mariana Islands
| `MQ` | Martinique
| `MR` | Mauritania
| `MS` | Montserrat
| `MT` | Malta
| `MU` | Mauritius
| `MV` | Maldives
| `MW` | Malawi
| `MX` | Mexico
| `MY` | Malaysia
| `MZ` | Mozambique
| `NA` | Namibia
| `NC` | New Caledonia
| `NE` | Niger
| `NG` | Nigeria
| `NI` | Nicaragua
| `NL` | Netherlands, The
| `NO` | Norway
| `NP` | Nepal
| `NR` | Nauru, Republic Of
| `NU` | Niue
| `NZ` | New Zealand
| `OM` | Oman
| `PA` | Panama
| `PE` | Peru
| `PF` | Tahiti
| `PG` | Papua New Guinea
| `PH` | Philippines, The
| `PK` | Pakistan
| `PL` | Poland
| `PR` | Puerto Rico
| `PT` | Portugal
| `PW` | Palau
| `PY` | Paraguay
| `QA` | Qatar
| `RE` | Reunion, Island Of
| `RO` | Romania
| `RS` | Serbia, Republic Of
| `RU` | Russian Federation, The
| `RW` | Rwanda
| `SA` | Saudi Arabia
| `SB` | Solomon Islands
| `SC` | Seychelles
| `SD` | Sudan
| `SE` | Sweden
| `SG` | Singapore
| `SH` | Saint Helena
| `SI` | Slovenia
| `SK` | Slovakia
| `SL` | Sierra Leone
| `SM` | San Marino
| `SN` | Senegal
| `SO` | Somalia
| `SR` | Suriname
| `SS` | South Sudan
| `ST` | Sao Tome And Principe
| `SV` | El Salvador
| `SY` | Syria
| `SZ` | Swaziland
| `TC` | Turks And Caicos Islands
| `TD` | Chad
| `TG` | Togo
| `TH` | Thailand
| `TJ` | Tajikistan
| `TL` | Timor Leste
| `TN` | Tunisia
| `TO` | Tonga
| `TR` | Turkey
| `TT` | Trinidad And Tobago
| `TV` | Tuvalu
| `TW` | Taiwan
| `TZ` | Tanzania
| `UA` | Ukraine
| `UG` | Uganda
| `US` | United States
| `UY` | Uruguay
| `UZ` | Uzbekistan
| `VA` | Vatican City State
| `VC` | St. Vincent
| `VE` | Venezuela
| `VG` | British Virgin Islands
| `VI` | U.S. Virgin Islands
| `VN` | Vietnam
| `VU` | Vanuatu
| `WS` | Samoa
| `XB` | Bonaire
| `XC` | Curacao
| `XE` | St. Eustatius
| `XM` | St. Maarten
| `XN` | Nevis
| `XS` | Somaliland, Rep Of (north Somalia)
| `XY` | St. Barthelemy
| `YE` | Yemen, Republic Of
| `YT` | Mayotte
| `ZA` | South Africa
| `ZM` | Zambia
| `ZW` | Zimbabwe

---


## States and Provinces


### United Arab Emirates

| Code | Name
| --- | ---
| `AB` | Abu Dhabi
| `AJ` | Ajman
| `DU` | Dubai
| `FU` | Fujairah
| `RA` | Ras al-Khaimah
| `SH` | Sharjah
| `UM` | Umm al-Qaiwain


### Canada

| Code | Name
| --- | ---
| `AB` | Alberta
| `BC` | British Columbia
| `MB` | Manitoba
| `NB` | New Brunswick
| `NL` | Newfoundland
| `NT` | Northwest Territories
| `NS` | Nova Scotia
| `NU` | Nunavut
| `ON` | Ontario
| `PE` | Prince Edward Island
| `QC` | Quebec
| `SK` | Saskatchewan
| `YT` | Yukon


### China, Peoples Republic

| Code | Name
| --- | ---
| `anhui` | Anhui
| `hainan` | Hainan
| `jiangxi` | Jiangxi
| `shanghai` | Shanghai
| `beijing` | Beijing
| `hebei` | Hebei
| `jilin` | Jilin
| `shanxi` | Shanxi
| `chongqing` | Chongqing
| `heilongjiang` | Heilongjiang
| `liaoning` | Liaoning
| `sichuan` | Sichuan
| `fujian` | Fujian
| `henan` | Henan
| `nei_mongol` | Nei Mongol
| `tianjin` | Tianjin
| `gansu` | Gansu
| `hubei` | Hubei
| `qinghai` | Qinghai
| `xinjiang` | Xinjiang
| `guangdong` | Guangdong
| `hunan` | Hunan
| `shaanxi` | Shaanxi
| `yunnan` | Yunnan
| `guizhou` | Guizhou
| `jiangsu` | Jiangsu
| `shandong` | Shandong
| `zhejiang` | Zhejiang


### India

| Code | Name
| --- | ---
| `AN` | Andaman & Nicobar (U.T)
| `AP` | Andhra Pradesh
| `AR` | Arunachal Pradesh
| `AS` | Assam
| `BR` | Bihar
| `CG` | Chattisgarh
| `CH` | Chandigarh (U.T.)
| `DD` | Daman & Diu (U.T.)
| `DL` | Delhi (U.T.)
| `DN` | Dadra and Nagar Haveli (U.T.)
| `GA` | Goa
| `GJ` | Gujarat
| `HP` | Himachal Pradesh
| `HR` | Haryana
| `JH` | Jharkhand
| `JK` | Jammu & Kashmir
| `KA` | Karnataka
| `KL` | Kerala
| `LD` | Lakshadweep (U.T)
| `MH` | Maharashtra
| `ML` | Meghalaya
| `MN` | Manipur
| `MP` | Madhya Pradesh
| `MZ` | Mizoram
| `NL` | Nagaland
| `OR` | Orissa
| `PB` | Punjab
| `PY` | Puducherry (U.T.)
| `RJ` | Rajasthan
| `SK` | Sikkim
| `TN` | Tamil Nadu
| `TR` | Tripura
| `UA` | Uttaranchal
| `UP` | Uttar Pradesh
| `WB` | West Bengal


### Mexico

| Code | Name
| --- | ---
| `AG` | Aguascalientes
| `BC` | Baja California
| `BS` | Baja California Sur
| `CM` | Campeche
| `CS` | Chiapas
| `CH` | Chihuahua
| `CO` | Coahuila
| `CL` | Colima
| `DF` | Ciudad de México
| `DG` | Durango
| `GT` | Guanajuato
| `GR` | Guerrero
| `HG` | Hidalgo
| `JA` | Jalisco
| `EM` | Estado de México
| `MI` | Michoacán
| `MO` | Morelos
| `NA` | Nayarit
| `NL` | Nuevo León
| `OA` | Oaxaca
| `PU` | Puebla
| `QE` | Querétaro
| `QR` | Quintana Roo
| `SL` | San Luis Potosí
| `SI` | Sinaloa
| `SO` | Sonora
| `TB` | Tabasco
| `TM` | Tamaulipas
| `TL` | Tlaxcala
| `VE` | Veracruz
| `YU` | Yucatán
| `ZA` | Zacatecas


### United States

| Code | Name
| --- | ---
| `AL` | Alabama
| `AK` | Alaska
| `AZ` | Arizona
| `AR` | Arkansas
| `CA` | California
| `CO` | Colorado
| `CT` | Connecticut
| `DE` | Delaware
| `DC` | District of Columbia
| `FL` | Florida
| `GA` | Georgia
| `HI` | Hawaii
| `ID` | Idaho
| `IL` | Illinois
| `IN` | Indiana
| `IA` | Iowa
| `KS` | Kansas
| `KY` | Kentucky
| `LA` | Louisiana
| `ME` | Maine
| `MD` | Maryland
| `MA` | Massachusetts
| `MI` | Michigan
| `MN` | Minnesota
| `MS` | Mississippi
| `MO` | Missouri
| `MT` | Montana
| `NE` | Nebraska
| `NV` | Nevada
| `NH` | New Hampshire
| `NJ` | New Jersey
| `NM` | New Mexico
| `NY` | New York
| `NC` | North Carolina
| `ND` | North Dakota
| `OH` | Ohio
| `OK` | Oklahoma
| `OR` | Oregon
| `PA` | Pennsylvania
| `RI` | Rhode Island
| `SC` | South Carolina
| `SD` | South Dakota
| `TN` | Tennessee
| `TX` | Texas
| `UT` | Utah
| `VT` | Vermont
| `VA` | Virginia
| `WA` | Washington State
| `WV` | West Virginia
| `WI` | Wisconsin
| `WY` | Wyoming
| `PR` | Puerto Rico


---


## Currencies

| Code | Name
| --- | ---
| `EUR` | Euro
| `AED` | UAE Dirham
| `USD` | US Dollar
| `XCD` | East Caribbean Dollar
| `AMD` | Dran
| `ANG` | Netherlands Antilles Guilder
| `AOA` | Kwanza
| `ARS` | Argentine Peso
| `AUD` | Australian Dollar
| `AWG` | Aruba Guilder
| `AZN` | Manat
| `BAM` | Convertible Marks
| `BBD` | Barbadian Dollar
| `BDT` | Taka
| `XOF` | CFA Franc West Africa
| `BGN` | Bulgarian Lev
| `BHD` | Bahraini Dinar
| `BIF` | Burundese Franc
| `BMD` | Bermudian Dollar
| `BND` | Brunei Dollar
| `BOB` | Boliviano
| `BRL` | Real
| `BSD` | Bahamian Dollar
| `BTN` | Ngultrum
| `BWP` | Pula
| `BYN` | Belarussian Ruble
| `BZD` | Belize Dollar
| `CAD` | Canadian Dollar
| `CDF` | Franc Congolais
| `XAF` | CFA Franc Central Africa
| `CHF` | Swiss Franc
| `NZD` | New Zealand Dollar
| `CLP` | New Chile Peso
| `CNY` | Yuan (Ren Min Bi)
| `COP` | Colombian Peso
| `CRC` | Costa Rican Colon
| `CUC` | Peso Convertible
| `CVE` | Cape Verde Escudo
| `CZK` | Czech Koruna
| `DJF` | Djibouti Franc
| `DKK` | Danish Krone
| `DOP` | Dominican Republic Peso
| `DZD` | Algerian Dinar
| `EGP` | Egyptian Pound
| `ERN` | Nakfa
| `ETB` | Birr
| `FJD` | Fijian Dollar
| `GBP` | Pound Sterling
| `GEL` | Georgian Lari
| `GHS` | Cedi
| `GMD` | Dalasi
| `GNF` | Guinea Franc
| `GTQ` | Quetzal
| `GYD` | Guyanan Dollar
| `HKD` | Hong Kong Dollar
| `HNL` | Lempira
| `HRK` | Croatian Kuna
| `HTG` | Gourde
| `HUF` | Forint
| `IDR` | Rupiah
| `ILS` | New Israeli Shekel
| `INR` | Indian Rupee
| `IRR` | Iranian Rial
| `ISK` | Icelandic Krona
| `JMD` | Jamaican Dollar
| `JOD` | Jordanian Dinar
| `JPY` | Yen
| `KES` | Kenyan Shilling
| `KGS` | Som
| `KHR` | Khmer Rial
| `KMF` | Comoros Franc
| `KPW` | North Korean Won
| `KRW` | Won
| `KWD` | Kuwaiti Dinar
| `KYD` | Cayman Islands Dollar
| `KZT` | Tenge
| `LAK` | Kip
| `LKR` | Sri Lankan Rupee
| `LRD` | Liberian Dollar
| `LSL` | Loti
| `LYD` | Libyan Dinar
| `MAD` | Moroccan Dirham
| `MDL` | Leu
| `MGA` | Ariary
| `MKD` | Denar
| `MMK` | Kyat
| `MNT` | Tugrik
| `MOP` | Pataca
| `MRO` | Ouguiya
| `MUR` | Mauritius Rupee
| `MVR` | Rufiyaa
| `MWK` | Kwacha
| `MXN` | Mexican Nuevo Peso
| `MYR` | Ringgit
| `MZN` | Mozambique Metical
| `NAD` | Namibian Dollar
| `XPF` | CFP Franc
| `NGN` | Naira
| `NIO` | Cordoba Oro
| `NOK` | Norwegian Krone
| `NPR` | Nepalese Rupee
| `OMR` | Omani Rial
| `PEN` | Nuevo Sol
| `PGK` | Kina
| `PHP` | Phillipines Peso
| `PKR` | Pakistani Rupee
| `PLN` | Zloty
| `PYG` | Guarani
| `QAR` | Qatar Rial
| `RSD` | Serbia, Dinars
| `RUB` | Russian Ruble
| `RWF` | Rwanda Franc
| `SAR` | Saudi Riyal
| `SBD` | Solomon Islands Dollar
| `SCR` | Seychelles Rupee
| `SDG` | Sudanese Pound
| `SEK` | Swedish Krona
| `SGD` | Singapore Dollar
| `SHP` | St. Helena Pound
| `SLL` | Leone
| `SOS` | Somali Shilling
| `SRD` | Suriname Dollar
| `SSP` | South Sudanese pound
| `STD` | Dobra
| `SYP` | Syrian Pound
| `SZL` | Lilangeni
| `THB` | Baht
| `TJS` | Somoni
| `TND` | Tunisian Dinar
| `TOP` | Pa'anga
| `TRY` | New Turkish Lira
| `TTD` | Trinidad and Tobago Dollar
| `TWD` | New Taiwan Dollar
| `TZS` | Tanzanian Shilling
| `UAH` | Hryvna
| `UYU` | Peso Uruguayo
| `UZS` | Sum
| `VEF` | Bolivar Fuerte
| `VND` | Dong
| `VUV` | Vanuatu Vatu
| `WST` | Tala
| `YER` | Yemeni Riyal
| `ZAR` | South African Rand
