import requests


def get_index_response():
    """Send GET request to Index API

    :return: response object
    """
    return requests.get("http://127.0.0.1:5000/")
