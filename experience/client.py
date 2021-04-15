import json

from experience.api.accounts import AccountsAPI
from experience.api.authentication import AuthenticationAPI
from experience.api.campaign import CampaignAPI
from experience.api.core import CoreAPI
from experience.api.hierarchy import HierarchyAPI
from experience.api.reports import ReportsAPI
from experience.api.tiers import TiersAPI
from experience.api.users import UsersAPI
from experience.configuration import environments


class Client:

    def __init__(self, **kwargs):
        #If access_token already exists
        if 'access_token' in kwargs:
            self.access_token = kwargs['access_token']

        #If user_email and password exists
        if 'user_email' and 'password' in kwargs:
            self.user_email = kwargs['user_email']
            self.password = kwargs['password']
            #call login method to get access_token
            access_token = AuthenticationAPI().login(self.user_email, self.password)
            self.access_token = json.loads(access_token)['auth_token']

        #Get Domain name
        self.base_url = environments[kwargs['environment']].get('default')

    def accounts(self):
        return AccountsAPI(self.access_token, self.base_url)

    def authentication(self):
        return AuthenticationAPI(self.base_url)

    def campaign(self):
        return CampaignAPI(self.access_token, self.base_url)

    def core(self):
        return CoreAPI(self.access_token, self.base_url)

    def hierarchy(self):
        return HierarchyAPI(self.access_token, self.base_url)

    def reports(self):
        return ReportsAPI(self.access_token, self.base_url)

    def tiers(self):
        return TiersAPI(self.access_token, self.base_url)

    def user(self):
        return UsersAPI(self.access_token, self.base_url)
