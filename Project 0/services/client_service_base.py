import math
from abc import ABC, abstractmethod
from typing import List
from entities.client import Client
from entities.account import Account


class ClientServiceBase(ABC):

    @abstractmethod
    def post_client(self, client: Client) -> bool:
        pass

    @abstractmethod
    def get_client(self, client_id: int) -> Client:
        pass

    @abstractmethod
    def get_clients(self) -> List[Client]:
        pass

    @abstractmethod
    def update_client(self, client_id: int, client: Client) -> bool:
        pass

    @abstractmethod
    def remove_client(self, client_id: int) -> bool:
        pass

    @abstractmethod
    def post_new_account_for(self, client_id: int, account: Account) -> bool:
        pass

    @abstractmethod
    def get_all_accounts_for(self, client_id: int, less_than: int = math.inf,
                             greater_than: int = -1) -> List[Account]:
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

    @abstractmethod
    def transfer_funds_to(self, client_id: int, account_from_id: int,
                          account_to_id: int, change: int) -> bool:
        pass
