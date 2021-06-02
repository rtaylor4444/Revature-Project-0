from typing import List

from daos.account_dao_base import AccountDAOBase
from daos.id_dictionary import IdDictionary
from entities.account import Account


class AccountDAOLocal(AccountDAOBase):
    def __init__(self) -> None:
        #client id -> accounts
        self.__account_dict = {}

    def __get_client_dict(self, client_id: int) -> IdDictionary:
        if client_id not in self.__account_dict:
            self.__account_dict.update({client_id: IdDictionary()})
        return self.__account_dict[client_id]

    def post_new_account_for(self, client_id: int, account: Account) -> bool:
        if account.get_amount() < 0:
            return False
        id_dict: IdDictionary = self.__get_client_dict(client_id)
        id_dict.insert_data(account)
        return True

    def get_all_accounts_for(self, client_id: int) -> List[Account]:
        id_dict: IdDictionary = self.__get_client_dict(client_id)
        return id_dict.get_all_data()

    def get_account_for(self, client_id: int, account_id: int) -> Account:
        id_dict: IdDictionary = self.__get_client_dict(client_id)
        return id_dict.get_data(account_id)

    def update_account_for(self, client_id: int, account_id: int, account: Account) -> bool:
        if account.get_amount() < 0:
            return False
        id_dict: IdDictionary = self.__get_client_dict(client_id)
        #Ids should match since we will overwrite the entire object
        old_account: Account = self.get_account_for(client_id, account_id)
        if old_account is None:
            return False
        account.set_id(old_account.get_id())
        return id_dict.update_data(account_id, account)

    def delete_account_for(self, client_id: int, account_id: int) -> bool:
        id_dict: IdDictionary = self.__get_client_dict(client_id)
        return id_dict.remove_data(account_id)

    def update_balance_for(self, client_id: int, account_id: int, change: int) -> bool:
        id_dict: IdDictionary = self.__get_client_dict(client_id)
        account: Account = id_dict.get_data(account_id)
        if account is None:
            return False
        return account.update_amount(change)
