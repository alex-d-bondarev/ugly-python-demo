import requests
from retrying import retry

DO_SOMETHING_API_URL = "http://127.0.0.1:5000/do_something_private"


class Something:
    """Class to manage something through API"""

    def __init__(self):
        self.process_id = 0

    def do_post(self, account_name):
        """Send POST request against given parameter

        :param account_name:
        :return:
        """
        request_data = {"by_name": account_name}
        response = requests.post(url=DO_SOMETHING_API_URL, data=request_data)
        if response.status_code == 202:
            self.process_id = response.json()["process_id"]

        return response

    def do_get_details(self):
        """Send POST request against given parameter

        :param account_name:
        :return:
        """
        url = f"{DO_SOMETHING_API_URL}/{self.process_id}"
        return requests.get(url=url).json()

    @retry(wait_fixed=100, stop_max_delay=5000)
    def wait_process_to_finish(self):
        """Wait for process to receive status 'done'
        or fail in 5 seconds
        """
        assert self.do_get_details()["status"] == "done"
