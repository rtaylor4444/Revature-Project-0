import math
from abc import ABC, abstractmethod
from entities.account import Account
from typing import List


class AccountDAOBase(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def post_new_account_for(self, client_id: int, account: Account) -> bool:
        pass

    @abstractmethod
    def get_all_accounts_for(self, client_id: int) -> List[Account]:
        pass

    @abstractmethod
    def get_account_for(self, client_id: int, account_id: int) -> Account:
        pass

    @abstractmethod
    def update_account_for(self, client_id: int, account_id: int, account: Account) -> bool:
        pass

    @abstractmethod
    def delete_account_for(self, client_id: int, account_id: int) -> bool:
        pass

    @abstractmethod
    def update_balance_for(self, client_id: int, account_id: int, change: int) -> bool:
        pass
