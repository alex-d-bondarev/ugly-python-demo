import pytest

from tests.improved.api.account import Account
from tests.improved.api.index import get_index_response
from tests.improved.api.something import Something

pytestmark = [pytest.mark.demo]


@pytest.mark.done
def test_index_api():
    index_response = get_index_response()
    assert index_response.status_code == 200


@pytest.mark.done
@pytest.mark.usefixtures("admin_account")
def test_admin_can_do_something(admin_account):
    admin_name = admin_account.name
    response = _do_something_as(account_name=admin_name)
    assert response.status_code == 202


@pytest.mark.done
@pytest.mark.usefixtures("admin_account")
def test_something_slow_as_admin(admin_account):
    admin_name = admin_account.name

    some_api_actions = Something()
    some_api_actions.do_post(account_name=admin_name)
    some_api_actions.wait_process_to_finish()

    json_response = some_api_actions.do_get_details()
    assert "done" == json_response["status"]


@pytest.mark.done
@pytest.mark.usefixtures("none_account")
def test_limited_account_can_do_nothing(none_account):
    account_name = none_account.name
    response = _do_something_as(account_name=account_name)
    assert response.status_code == 403


@pytest.fixture(scope="function")
def admin_account():
    """Fixture for creating and deleting admin account

    """
    admin_name = "mr_admin"
    account = _create_admin_account(admin_name)

    yield account

    account.delete()


@pytest.fixture(scope="function")
def none_account():
    """Fixture for creating and deleting admin account

    """
    account_name = "mr_none"
    account = _create_none_account(account_name)

    yield account

    account.delete()


def _create_admin_account(account_name):
    return _create_account_with_name_and_role(account_name, "admin")


def _create_none_account(account_name):
    return _create_account_with_name_and_role(account_name, "none")


def _create_account_with_name_and_role(name, role):
    account = Account(name=name)
    account.create()
    account.assign_role(role)
    return account


def _do_something_as(account_name):
    some_api_actions = Something()
    response = some_api_actions.do_post(account_name=account_name)
    return response
