import time

import pytest
import requests as requests

pytestmark = [pytest.mark.demo]


@pytest.mark.done
def test_something_slow_as_admin():
    r = requests.get('http://127.0.0.1:5000/')
    assert r.status_code == 200

    account_url = "http://127.0.0.1:5000/account"

    account_name = "demo_test"

    new_account = dict()
    new_account["name"] = account_name
    new_account["number"] = 123
    response = requests.request("POST", account_url, data=new_account)

    new_role = dict()
    new_role["name"] = account_name
    new_role["role"] = "admin"
    response = requests.request("PUT", account_url, data=new_role)

    do_somethin_url = "http://127.0.0.1:5000/do_something_private"
    do_something_data = dict()
    do_something_data["by_name"] = account_name
    response = requests.request("POST", do_somethin_url, data=do_something_data)
    assert response.status_code == 202

    time.sleep(4)

    assert _execute_process_status_decision_helper(response.status_code, do_somethin_url, r, response)

    delete_account = dict()
    delete_account["name"] = "demo_test"
    response = requests.request("DELETE", account_url, data=delete_account)


@pytest.mark.done
def test_something_slow_with_limited_permissions():
    r = requests.get('http://127.0.0.1:5000/')
    assert r.status_code == 200

    account_url = "http://127.0.0.1:5000/account"

    account_name = "demo_test"

    new_account = dict()
    new_account["name"] = account_name
    new_account["number"] = 123
    response = requests.request("POST", account_url, data=new_account)

    new_role = dict()
    new_role["name"] = account_name
    new_role["role"] = "none"
    response = requests.request("PUT", account_url, data=new_role)

    do_somethin_url = "http://127.0.0.1:5000/do_something_private"
    do_something_data = dict()
    do_something_data["by_name"] = account_name
    response = requests.request("POST", do_somethin_url, data=do_something_data)
    assert response.status_code == 403

    assert _execute_process_status_decision_helper(response.status_code, do_somethin_url, r, response)

    delete_account = dict()
    delete_account["name"] = "demo_test"
    response = requests.request("DELETE", account_url, data=delete_account)


def _execute_process_status_decision_helper(code, do_somethin_url, r, response):
    if code == 403:
        return True
    else:
        process_id = response.json()["process_id"]
        r = requests.get(do_somethin_url + "/" + str(process_id))
        return "done" == r.json()["status"]
