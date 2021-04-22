import json

from experience.api.accounts import AccountsAPI
from experience.api.authentication import AuthenticationAPI
from experience.api.core import CoreAPI
from experience.api.hierarchy import HierarchyAPI
from experience.api.reports import ReportsAPI
from experience.api.tiers import TiersAPI
from experience.api.users import UsersAPI
from experience.api.ingest_transaction import IngestTransactionAPI
from experience.configuration import environments


class Client:

    def __init__(self, **kwargs):
        self.access_token = None

        # If access_token already exists
        if 'access_token' in kwargs:
            self.access_token = kwargs['access_token']

        if 'environment' in kwargs:
            # Get Domain name
            self.base_url = environments[kwargs['environment']].get('default')

        #To form base url with subdomain and domain name
        if 'domain' in kwargs:
            self.domain = kwargs['domain']

        # If user_email and password exists
        if 'user_email' and 'password' in kwargs:
            self.user_email = kwargs['user_email']
            self.password = kwargs['password']
            # call login method to get access_token
            access_token = AuthenticationAPI(self.access_token, self.base_url).login(self.user_email, self.password)
            if "error" not in access_token:
                self.access_token = json.loads(access_token)['auth_token']

        #To Get current user details by calling current_user_details method
        self.base_url = 'https://api.' + self.domain + '.experience.com'
        self.user_details = AuthenticationAPI(self.access_token, self.base_url).current_user_details()

    def form_base_url(self, subdomain):
        # To form base url with subdomain and domain name
        if self.domain:
            self.base_url = 'https://'+ subdomain + self.domain + '.experience.com'
            return self.base_url

    def accounts(self):
        self.form_base_url('api.')
        return AccountsAPI(self.access_token, self.base_url, self.user_details)

    def authentication(self):
        self.form_base_url('api.')
        return AuthenticationAPI(self.access_token, self.base_url)

    def core(self):
        self.form_base_url('api.')
        return CoreAPI(self.access_token, self.base_url)

    def hierarchy(self):
        self.form_base_url('api.')
        return HierarchyAPI(self.access_token, self.base_url)

    def reports(self):
        self.form_base_url('reports.')
        return ReportsAPI(self.access_token, self.base_url)

    def tiers(self):
        self.form_base_url('api.')
        return TiersAPI(self.access_token, self.base_url)

    def user(self):
        self.form_base_url('api.')
        return UsersAPI(self.access_token, self.base_url, self.user_details)

    def ingest_transaction(self):
        self.form_base_url('integrations.')
        return IngestTransactionAPI(self.access_token, self.base_url)
