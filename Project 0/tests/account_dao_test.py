from daos.account_dao_base import AccountDAOBase
from daos.account_dao_local import AccountDAOLocal
from daos.account_dao_postgres import AccountDAOPostgres
from daos.client_dao_postgres import ClientDAOPostgres
from entities.account import Account
from entities.client import Client
from unittest import TestCase

# Local Settings
# account_dao: AccountDAOBase = AccountDAOLocal()
# client_id: int = 1


# Database Settings
account_dao: AccountDAOPostgres = AccountDAOPostgres()
client_dao: ClientDAOPostgres = ClientDAOPostgres()
client: Client = Client("Test Client")
client_dao.post_client(client)
client_id = client.get_id()


def test_post_new_account_for():
    account: Account = Account(client_id, 100)
    assert account_dao.post_new_account_for(client_id, account)


def test_post_new_account_for_invalid():
    account: Account = Account(client_id, -100)
    assert not account_dao.post_new_account_for(client_id, account)


def test_get_all_accounts_for():
    account: Account = Account(client_id, 75)
    account_dao.post_new_account_for(client_id, account)
    account_list = account_dao.get_all_accounts_for(client_id)
    TestCase().assertDictEqual({"Owner": client_id,
                                "Account": account_list[0].get_id(),
                                "Balance": account_list[0].get_amount()},
                               account_list[0].to_dict())
    TestCase().assertDictEqual({"Owner": client_id,
                                "Account": account_list[1].get_id(),
                                "Balance": account_list[1].get_amount()},
                               account_list[1].to_dict())


def test_get_account_for():
    account: Account = Account(client_id, 50)
    account_dao.post_new_account_for(client_id, account)
    result: Account = account_dao.get_account_for(client_id, account.get_id())
    TestCase().assertDictEqual(account.to_dict(), result.to_dict())


def test_update_account_for_pass():
    account_old: Account = Account(client_id, 25)
    account_dao.post_new_account_for(client_id, account_old)
    account_new: Account = Account(client_id, 125)
    is_success: bool = account_dao.update_account_for(client_id, account_old.get_id(), account_new)
    assert is_success and account_old.get_id() == account_new.get_id()
    assert account_dao.get_account_for(client_id, account_new.get_id()).get_amount() == account_new.get_amount()


def test_update_account_for_fail():
    account_new: Account = Account(client_id, 200)
    assert not account_dao.update_account_for(client_id, -1, account_new)


def test_update_account_for_invalid():
    account_old: Account = Account(client_id, 25)
    account_dao.post_new_account_for(client_id, account_old)
    account_new: Account = Account(client_id, -125)
    assert not account_dao.update_account_for(client_id, account_old.get_id(), account_new)


def test_delete_account_for():
    account_new: Account = Account(client_id, 200)
    account_dao.post_new_account_for(client_id, account_new)
    account_dao.delete_account_for(client_id, account_new.get_id())
    assert account_dao.get_account_for(client_id, account_new.get_id()) is None


def test_update_balance_for_pass():
    account_new: Account = Account(client_id, 200)
    account_dao.post_new_account_for(client_id, account_new)
    is_success: bool = account_dao.update_balance_for(client_id, account_new.get_id(), -200)
    result: Account = account_dao.get_account_for(client_id, account_new.get_id())
    assert is_success and result.get_amount() == 0


def test_update_balance_for_invalid():
    assert not account_dao.update_balance_for(client_id, -1, -200)


def test_update_balance_for_fail():
    account_new: Account = Account(client_id, 200)
    account_dao.post_new_account_for(client_id, account_new)
    assert not account_dao.update_balance_for(client_id, account_new.get_id(), -201)
