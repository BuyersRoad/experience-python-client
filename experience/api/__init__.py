
"""
 Experience.com
 ----------------------------
 We believe that experience is everything. Amazing experiences create customers for life, and poor ones destroy brands
 and businesses. That’s why Experience.com has built the most impactful Experience Management Platform (XMP) available
 anywhere, with features to drive operational and behavioral change, in real-time, during the moments that matter.
 XMP delivers impactful business outcomes including increased customer satisfaction, brand loyalty,
 online reputation and visibility, as well as improved employee engagement, and
 compliance - making every experience matter more.

 Experience Python SDK
 ----------------------------
 `experience` is a Python wrapper for the Developer Portal API. The goal of the project is to make it possible to write
 clean,fast, Pythonic code when interacting with Developer Portal API programmatically. The wrapper tries to keep API
 calls to a minimum. Wherever it makes sense objects are cached, and attributes of objects that would trigger an API
 call are evaluated lazily.The wrapper supports both reading and writing from the API.

 Versions
 ----------------------------
    * python 3.5 and above

 Set Up
 ----------------------------
 Make sure you changed the present working directory to the folder you are going to create your Python library in
 (cd <path/to/folder>).Go ahead and create a virtual environment by typing:


     python3 -m venv venv

 Once it is created, you must now activate the environment by using:


     source venv/bin/activate

 Installing
 ----------------------------


     pip install -e git+git@github.com:BuyersRoad/experience-python-client.git@SSV2-1926-experience-python-sdk#egg=experience-python-client

 Usage
 ----------------------------
 First, create a `Client` object:

     >>> from experience.client import Client
     ... client = Client(access_token='access_token', domain='domain name')

 (or)

     >>> from experience.client import Client
     ... client = Client(user_email='email@gmail.com', password='password', domain='domain name')

 Domains
 ----------------------------
 `experience_python_client` will make request to:


     https://{subdomain}.{domain}/{endpoint}
 You have to pass domain while Invoking `Client` Class , subdomain and endpoint will fetch automatically
 Domain
    * Sandbox
    * Prod


     https://{subdomain}.{sandbox}/{endpoint}

 """