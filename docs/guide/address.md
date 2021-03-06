## `Validation`

```python
import purplship
from purplship.core.models import AddressValidationRequest

request = AddressValidationRequest(...)

validation, messages = purplship.Address.validate(request).from_(carrier_gateway).parse()
```

### Parameters


#### AddressValidationRequest

| Name | Type | Description 
| --- | --- | --- |
| `address` | [Address](#address) | **required**


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


### Response


#### AddressValidationDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `success` | `bool` | **required**
| `complete_address` | [Address](#address) | 


#### Message

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `message` | Union[str, Any] | 
| `code` | `str` | 
| `details` | `dict` | 


---

### Code sample

```python
import purplship
from purplship.core.models import AddressValidationRequest, Address

address = Address(
    postal_code="V6M2V9",
    city="Vancouver",
    country_code="CA",
    state_code="BC",
    address_line1="5840 Oak St"
)

request = purplship.Address.validate(
    AddressValidationRequest(address=address)
)

tracking_details_list, messages = request.from_(carrier_gateway).parse()
```
