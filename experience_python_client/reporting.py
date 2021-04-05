import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from experience_python_client.api import Report, Hierarchy
from experience_python_client.api import Authentication


class Client:
    def __init__(self, access_token):
        self.access_token = access_token

    @staticmethod
    def login():
        return Authentication()

    def report(self):
        return Report(self.access_token)

    def hierarchy(self):
        return Hierarchy(self.access_token)
