from typing import List
from services.client_service_base import ClientServiceBase
from services.client_service import ClientService
from daos.account_dao_base import AccountDAOBase
from daos.account_dao_local import AccountDAOLocal
from daos.account_dao_postgres import AccountDAOPostgres
from daos.client_dao_base import ClientDAOBase
from daos.client_dao_local import ClientDAOLocal
from daos.client_dao_postgres import ClientDAOPostgres
from entities.client import Client
from entities.account import Account
from unittest import TestCase
from exceptions.invalid_param_exception import InvalidParamError
from exceptions.not_found_exception import ResourceNotFoundError

# Local Settings
# client_dao: ClientDAOBase = ClientDAOLocal()
# account_dao: AccountDAOBase = AccountDAOLocal()

# Database Settings
client_dao: ClientDAOBase = ClientDAOPostgres()
account_dao: AccountDAOBase = AccountDAOPostgres()

client_service: ClientServiceBase = ClientService(client_dao, account_dao)


def test_post_client_pass():
    client: Client = Client("Test")
    is_success: bool = client_service.post_client(client)
    assert is_success and not client.get_id() == 0


# Clients must have a name + throw error
def test_post_client_invalid():
    try:
        client: Client = Client("")
        client_service.post_client(client)
        assert False
    except InvalidParamError:
        assert True


def test_get_client_pass():
    client: Client = Client("Get me")
    client_service.post_client(client)
    assert client_service.get_client(client.get_id())


def test_get_client_invalid():
    try:
        client_service.get_client(-1)
        assert False
    except ResourceNotFoundError:
        assert True


def test_get_clients():
    client_list: List[Client] = client_service.get_clients()
    assert len(client_list) > 0


def test_update_client_fail():
    try:
        client_service.update_client(-1, Client("Failure"))
        assert False
    except ResourceNotFoundError:
        assert True


def test_update_client():
    client: Client = Client("Update me")
    client_service.post_client(client)
    new_client: Client = Client("Updated")
    assert client_service.update_client(client.get_id(), new_client)
    assert client.get_id() == new_client.get_id()


def test_update_client_invalid():
    client: Client = Client("Update me")
    client_service.post_client(client)
    new_client: Client = Client("")
    try:
        client_service.update_client(client.get_id(), new_client)
        assert False
    except InvalidParamError:
        assert True


def test_remove_client():
    client: Client = Client("Remove me")
    client_service.post_client(client)
    assert client_service.remove_client(client.get_id())
    try:
        client_service.remove_client(client.get_id())
        assert False
    except ResourceNotFoundError:
        assert True


# must throw error code - client does not exist
def test_post_new_account_for_invalid1():
    try:
        client_service.post_new_account_for(-1, Account(-1))
        assert False
    except ResourceNotFoundError:
        assert True


# must throw error code - account cannot have negative balance
def test_post_new_account_for_invalid2():
    client: Client = Client("post account")
    client_service.post_client(client)
    try:
        client_service.post_new_account_for(client.get_id(), Account(0, -1))
        assert False
    except InvalidParamError:
        assert True


def test_post_new_account_for_pass():
    client: Client = Client("post account")
    client_service.post_client(client)
    account: Account = Account(client.get_id(), 100)
    assert client_service.post_new_account_for(client.get_id(), account)
    assert account.get_owner_id() == client.get_id()


# must throw error code - client does not exist
def test_get_all_accounts_for_invalid1():
    try:
        client_service.get_all_accounts_for(-1)
        assert False
    except ResourceNotFoundError:
        assert True


def test_get_all_accounts_for_pass():
    client: Client = Client("multi account")
    client_service.post_client(client)
    account1: Account = Account(client.get_id(), 10)
    account2: Account = Account(client.get_id(), 20)
    client_service.post_new_account_for(client.get_id(), account1)
    client_service.post_new_account_for(client.get_id(), account2)
    account_list: List[Account] = client_service.get_all_accounts_for(client.get_id())
    assert len(account_list) == 2
    TestCase().assertDictEqual(account_list[0].to_dict(), account1.to_dict())
    TestCase().assertDictEqual(account_list[1].to_dict(), account2.to_dict())


def test_get_all_accounts_for_filter():
    client: Client = Client("filter account")
    client_service.post_client(client)
    account1: Account = Account(client.get_id(), 10)
    account2: Account = Account(client.get_id(), 20)
    client_service.post_new_account_for(client.get_id(), account1)
    client_service.post_new_account_for(client.get_id(), account2)
    account_list: List[Account] = client_service.get_all_accounts_for(client.get_id(), 20, 0)
    assert len(account_list) == 1
    TestCase().assertDictEqual(account_list[0].to_dict(), account1.to_dict())


# client and account id invalid throw error for client
def test_get_account_for_invalid_client():
    try:
        client_service.get_account_for(-1, -1)
        assert False
    except ResourceNotFoundError:
        assert True


# account id invalid throw error for account
def test_get_account_for_invalid_account():
    try:
        client: Client = Client("no account")
        client_service.post_client(client)
        client_service.get_account_for(client.get_id(), -1)
        assert False
    except ResourceNotFoundError:
        assert True


def test_get_account_for_pass():
    client: Client = Client("test account")
    client_service.post_client(client)
    account: Account = Account(client.get_id(), 100)
    client_service.post_new_account_for(client.get_id(), account)
    result: Account = client_service.get_account_for(client.get_id(), account.get_id())
    assert result is not None
    TestCase().assertDictEqual(result.to_dict(), account.to_dict())


# client and account id invalid throw error for client
def test_update_account_for_invalid_client():
    try:
        account: Account = Account(0, 0)
        client_service.update_account_for(-1, -1, account)
        assert False
    except ResourceNotFoundError:
        assert True


# account id invalid throw error for account
def test_update_account_for_invalid_account():
    try:
        client: Client = Client("no account")
        client_service.post_client(client)
        account: Account = Account(0, 0)
        client_service.update_account_for(client.get_id(), -1, account)
        assert False
    except ResourceNotFoundError:
        assert True


# account amount is negative throw error for account
def test_update_account_for_invalid_balance():
    client: Client = Client("no account")
    client_service.post_client(client)
    account_old: Account = Account(client.get_id(), 0)
    client_service.post_new_account_for(client.get_id(), account_old)
    account_new: Account = Account(client.get_id(), -1)
    try:
        client_service.update_account_for(client.get_id(), account_old.get_id(), account_new)
        assert False
    except InvalidParamError:
        assert True


def test_update_account_for_pass():
    client: Client = Client("update account")
    client_service.post_client(client)
    account_old: Account = Account(client.get_id(), 0)
    client_service.post_new_account_for(client.get_id(), account_old)
    account_new: Account = Account(client.get_id(), 100)
    assert client_service.update_account_for(client.get_id(), account_old.get_id(), account_new)
    assert account_old.get_id() == account_new.get_id()


def test_delete_account_for():
    client: Client = Client("delete account")
    client_service.post_client(client)
    account: Account = Account(client.get_id(), 100)
    client_service.post_new_account_for(client.get_id(), account)
    assert client_service.delete_account_for(client.get_id(), account.get_id())
    try:
        client_service.delete_account_for(client.get_id(), account.get_id())
    except ResourceNotFoundError:
        assert True


def test_delete_account_for_invalid():
    client: Client = Client("delete account")
    client_service.post_client(client)
    try:
        client_service.delete_account_for(client.get_id(), -1)
        assert False
    except ResourceNotFoundError:
        assert True


def test_delete_client_with_accounts():
    client: Client = Client("delete account")
    client_service.post_client(client)
    account: Account = Account(client.get_id(), 100)
    client_service.post_new_account_for(client.get_id(), account)
    assert client_service.remove_client(client.get_id())
    try:
        client_service.delete_account_for(client.get_id(), account.get_id())
        assert False
    except ResourceNotFoundError:
        assert True


# client and account id invalid throw an error
def test_deposit_amount_to_invalid_client():
    try:
        client_service.update_balance_for(-1, -1, 0)
        assert False
    except ResourceNotFoundError:
        assert True


# account id invalid throw an error
def test_deposit_amount_to_invalid_account():
    try:
        client: Client = Client("deposit account")
        client_service.post_client(client)
        client_service.update_balance_for(client.get_id(), -1, 0)
        assert False
    except ResourceNotFoundError:
        assert True


def test_deposit_amount_to():
    client: Client = Client("deposit account")
    client_service.post_client(client)
    account: Account = Account(client.get_id(), 100)
    client_service.post_new_account_for(client.get_id(), account)
    assert client_service.update_balance_for(client.get_id(), account.get_id(), 100)
    result: Account = client_service.get_account_for(client.get_id(), account.get_id())
    assert result.get_amount() == 200


# throw an error when withdrawing more than account amount
def test_insufficient_funds():
    client: Client = Client("withdraw account")
    client_service.post_client(client)
    account: Account = Account(client.get_id(), 100)
    client_service.post_new_account_for(client.get_id(), account)
    try:
        client_service.update_balance_for(client.get_id(), account.get_id(), -101)
        assert False
    except InvalidParamError:
        assert True


def test_withdraw_amount_from():
    client: Client = Client("withdraw account")
    client_service.post_client(client)
    account: Account = Account(client.get_id(), 100)
    client_service.post_new_account_for(client.get_id(), account)
    assert client_service.update_balance_for(client.get_id(), account.get_id(), -100)
    result: Account = client_service.get_account_for(client.get_id(), account.get_id())
    assert result.get_amount() == 0


# client and account id invalid throw an error
def test_transfer_invalid_client():
    try:
        client_service.transfer_funds_to(-1, -1, -1, 0)
        assert False
    except ResourceNotFoundError:
        assert True


# account id invalid throw an error
# (from account if both or from missing)
# (to account if from is present but to is missing)
def test_transfer_invalid_account():
    client: Client = Client("transfer account")
    client_service.post_client(client)
    try:
        client_service.transfer_funds_to(client.get_id(), -1, -1, 0)
        assert False
    except ResourceNotFoundError:
        assert True

    account: Account = Account(client.get_id(), 100)
    client_service.post_new_account_for(client.get_id(), account)
    try:
        client_service.transfer_funds_to(client.get_id(), -1, account.get_id(), 0)
        assert False
    except ResourceNotFoundError:
        assert True

    try:
        client_service.transfer_funds_to(client.get_id(), account.get_id(), -1, 0)
        assert False
    except ResourceNotFoundError:
        assert True


# throw error that from account lacks funds
# then throw error that to account lacks funds
def test_transfer_insufficient_funds():
    client: Client = Client("transfer account")
    client_service.post_client(client)
    account_from: Account = Account(client.get_id(), 100)
    account_to: Account = Account(client.get_id(), 0)
    client_service.post_new_account_for(client.get_id(), account_from)
    client_service.post_new_account_for(client.get_id(), account_to)
    try:
        client_service.transfer_funds_to(client.get_id(), account_from.get_id(),
                                         account_to.get_id(), 101)
        assert False
    except InvalidParamError:
        assert True

    try:
        client_service.transfer_funds_to(client.get_id(), account_from.get_id(),
                                         account_to.get_id(), -101)
        assert False
    except InvalidParamError:
        assert True


def test_transfer_funds():
    client: Client = Client("transfer account")
    client_service.post_client(client)
    account_from: Account = Account(client.get_id(), 100)
    account_to: Account = Account(client.get_id(), 0)
    client_service.post_new_account_for(client.get_id(), account_from)
    client_service.post_new_account_for(client.get_id(), account_to)
    assert client_service.transfer_funds_to(client.get_id(), account_from.get_id(),
                                            account_to.get_id(), 100)
    result_from = client_service.get_account_for(client.get_id(), account_from.get_id())
    assert result_from.get_amount() == 0
    result_to = client_service.get_account_for(client.get_id(), account_to.get_id())
    assert result_to.get_amount() == 100
