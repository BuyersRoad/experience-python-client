# experience-python-client
We believe that experience is everything. Amazing experiences create customers for life, and poor ones destroy brands and businesses. That’s why Experience.com has built the most impactful Experience Management Platform (XMP) available anywhere, with features to drive operational and behavioral change, in real-time, during the moments that matter. XMP delivers impactful business outcomes including increased customer satisfaction, brand loyalty, online reputation and visibility, as well as improved employee engagement, and compliance - making every experience matter more.
## Versions
* python 3.5 and above
## API Documentation
* [Documentation](http://localhost:63342/experience-python-client/docs/api/index.html?_ijt=f8dh1n522cbe5ds0nagrobuilg)
## Building
`python setup.py bdist_wheel`
## Installing
`pip install dist/experience_python_client-0.1.0-py3-none-any.whl`
## Usage
To call an endpoint you must create a `Client` object.

`client = Client(access_token=access_token, environment='')`
    
## Example
Now let’s call your first Experience API. create a new file called new.py, and copy the following code into that file:

```from experience_python_client.constants import access_token
from experience_python_client.reporting import Client

# Invoking the Client class by passing access token or (user_email ,password) and environment
client = Client(user_email="xxx@gmail.com", password="xxx@123", environment='sandbox')
tier_api = client.tiers()
core_api = client.core()

# To get all account id with name
account_id = core_api.get_all_account_id_and_name()
# To print account id
result_status(account_id)
  