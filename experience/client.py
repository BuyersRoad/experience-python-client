from experience.api.accounts import AccountsAPI
from experience.api.authentication import AuthenticationAPI
from experience.api.campaign import CampaignAPI
from experience.api.core import CoreAPI
from experience.api.hierarchy import HierarchyAPI
from experience.api.reports import ReportsAPI
from experience.api.tiers import TiersAPI
from experience.api.users import UsersAPI


class Client:
    def __init__(self, access_token):
        self.access_token = access_token

    def accounts(self):
        return AccountsAPI(self.access_token)

    def authentication(self):
        return AuthenticationAPI()

    def campaign(self):
        return CampaignAPI(self.access_token)

    def core(self):
        return CoreAPI(self.access_token)

    def hierarchy(self):
        return HierarchyAPI(self.access_token)

    def reports(self):
        return ReportsAPI(self.access_token)

    def tiers(self):
        return TiersAPI(self.access_token)

    def user(self):
        return UsersAPI(self.access_token)
