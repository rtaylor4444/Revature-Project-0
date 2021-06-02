from entities.account import Account
from unittest import TestCase

client_id: int = 0


def test_set_id():
    account: Account = Account(client_id)
    account.set_id(1)
    assert account.get_id() == 1


def test_deposit_funds():
    account: Account = Account(client_id, 0)
    account.update_amount(100)
    assert account.get_amount() == 100


def test_withdraw_funds_valid():
    account: Account = Account(client_id, 100)
    account.update_amount(-100)
    assert account.get_amount() == 0


def test_withdraw_funds_invalid():
    account: Account = Account(client_id, 0)
    assert not account.update_amount(-100)


def test_to_dict():
    account: Account = Account(client_id, 0)
    result_dict = account.to_dict()
    TestCase().assertDictEqual({"Owner": client_id, "Account": 0, "Balance": account.get_amount()}, result_dict)

