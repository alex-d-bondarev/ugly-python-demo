import requests

ACCOUNT_API_URL = "http://127.0.0.1:5000/account"


class Account:
    """Class to manage accounts through API"""

    def __init__(self, name, number=111):
        self.name = name
        self.number = number

    def create(self):
        """Create new Account"""
        request_data = {"name": self.name, "number": self.number}
        requests.post(url=ACCOUNT_API_URL, data=request_data)

    def assign_role(self, role):
        """Assign given role to account

        :param role:
        """
        request_data = {"name": self.name, "role": role}
        requests.put(url=ACCOUNT_API_URL, data=request_data)

    def delete(self):
        """Delete current account"""
        request_data = {"name": self.name}
        requests.delete(url=ACCOUNT_API_URL, data=request_data)
