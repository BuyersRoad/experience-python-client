# experience-python-client
We believe that experience is everything. Amazing experiences create customers for life, and poor ones destroy brands and businesses. That’s why Experience.com has built the most impactful Experience Management Platform (XMP) available anywhere, with features to drive operational and behavioral change, in real-time, during the moments that matter. XMP delivers impactful business outcomes including increased customer satisfaction, brand loyalty, online reputation and visibility, as well as improved employee engagement, and compliance - making every experience matter more.
## Versions
* python 3.5 and above
## API Documentation
* [Hierarchy](experience_python_client/doc/hierarchy.md)
* [Reporting](experience_python_client/doc/report.md)
## Building
`python setup.py bdist_wheel`
## Installing
`pip install dist/experience_python_client-0.1.0-py3-none-any.whl`
## Usage
To call an endpoint you must create a `Client` object.

`client = Client(access_token=access_token)`
    
## Example
Now let’s call your first Experience API. create a new file called new.py, and copy the following code into that file:

```from experience_python_client.constants import access_token
from experience_python_client.reporting import Client

client = Client(access_token=access_token)
report = client.report()
result = report.activity_feed(access_token=access_token, id='1892', page='3')

if result.is_success():
    print(result)
 
elif result.is_error():
    print('Error calling Report.activity_feed')
    errors = result.errors
    print(errors)
  