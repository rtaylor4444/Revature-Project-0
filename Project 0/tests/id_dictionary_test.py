from daos.id_dictionary import IdDictionary
from entities.account import Account
from unittest import TestCase


def test_verify_data():
    nums: IdDictionary = IdDictionary()
    nums.insert_data(0)
    assert nums.verify_data(1)


def test_verify_data_fail():
    nums: IdDictionary = IdDictionary()
    nums.insert_data(0)
    assert not nums.verify_data(2)


def test_get_data():
    nums: IdDictionary = IdDictionary()
    nums.insert_data(100)
    assert nums.get_data(1) == 100


def test_get_data_fail():
    nums: IdDictionary = IdDictionary()
    nums.insert_data(100)
    result: int = nums.get_data(2)
    assert result is None


def test_get_all_data1():
    nums: IdDictionary = IdDictionary()
    nums.insert_data(100)
    nums.insert_data(50)
    nums.insert_data(25)
    result_list = nums.get_all_data()
    TestCase().assertListEqual([100, 50, 25], result_list)


def test_get_all_data2():
    nums: IdDictionary = IdDictionary()
    nums.insert_data(100)
    nums.insert_data(50)
    nums.insert_data(25)
    nums.remove_data(1)
    result_list = nums.get_all_data()
    TestCase().assertListEqual([50, 25], result_list)


def test_remove_data():
    nums: IdDictionary = IdDictionary()
    nums.insert_data(100)
    assert nums.remove_data(1)


def test_remove_data_ensure():
    nums: IdDictionary = IdDictionary()
    nums.insert_data(100)
    if not nums.remove_data(1):
        assert False
    result = nums.get_data(1)
    assert result is None


def test_remove_data_fail():
    nums: IdDictionary = IdDictionary()
    assert not nums.remove_data(1)


def test_update_data():
    nums: IdDictionary = IdDictionary()
    nums.insert_data(0)
    assert nums.update_data(1, 100)


def test_update_data_fail():
    nums: IdDictionary = IdDictionary()
    assert not nums.update_data(1, 100)


def test_update_data_ensure():
    nums: IdDictionary = IdDictionary()
    nums.insert_data(0)
    if not nums.update_data(1, 100):
        assert False
    assert nums.get_data(1) == 100


#removing and replacing that an id
def test_ids_management():
    accounts: IdDictionary = IdDictionary()
    account_old: Account = Account(0)
    accounts.insert_data(account_old)
    accounts.remove_data(1)
    account_new: Account = Account(0, 25)
    accounts.insert_data(account_new)
    assert account_old.get_id() == account_new.get_id()
