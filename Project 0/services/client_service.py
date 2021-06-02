import math
from typing import List
from entities.account import Account
from entities.client import Client
from services.client_service_base import ClientServiceBase
from daos.client_dao_base import ClientDAOBase
from daos.account_dao_base import AccountDAOBase
from exceptions.invalid_param_exception import InvalidParamError
from exceptions.not_found_exception import ResourceNotFoundError


class ClientService(ClientServiceBase):

    def __init__(self, client_dao: ClientDAOBase, account_dao: AccountDAOBase):
        self.client_dao = client_dao
        self.account_dao = account_dao

    def post_client(self, client: Client) -> bool:
        if not self.client_dao.post_client(client):
            raise InvalidParamError("Name must be 3 or more characters")
        return True

    def get_client(self, client_id: int) -> Client:
        client: Client = self.client_dao.get_client(client_id)
        if client is None:
            raise ResourceNotFoundError("Invalid client ID")
        return client

    def get_clients(self) -> List[Client]:
        return self.client_dao.get_clients()

    def update_client(self, client_id: int, client: Client) -> bool:
        # Verify client ID
        self.get_client(client_id)
        if not self.client_dao.update_client(client_id, client):
            raise InvalidParamError("Name must be 3 or more characters")
        return True

    def remove_client(self, client_id: int) -> bool:
        # Remove all associated accounts if any
        accounts: List[Account] = self.get_all_accounts_for(client_id)
        for a in accounts:
            self.delete_account_for(client_id, a.get_id())
        # Finally remove client
        return self.client_dao.remove_client(client_id)

    def post_new_account_for(self, client_id: int, account: Account) -> bool:
        # Verify client ID
        self.get_client(client_id)
        if not self.account_dao.post_new_account_for(client_id, account):
            raise InvalidParamError("Accounts cannot have a negative balance")
        return True

    def get_all_accounts_for(self, client_id: int, less_than: int = math.inf, greater_than: int = -1) -> List[Account]:
        # Verify client ID
        self.get_client(client_id)
        account_list: List[Account] = self.account_dao.get_all_accounts_for(client_id)
        result_list = []
        for a in account_list:
            amount: int = a.get_amount()
            if greater_than < amount < less_than:
                result_list.append(a)

        return result_list

    def get_account_for(self, client_id: int, account_id: int) -> Account:
        # Verify client ID
        self.get_client(client_id)
        account: Account = self.account_dao.get_account_for(client_id, account_id)
        if account is None:
            raise ResourceNotFoundError("Invalid account ID")
        return account

    def update_account_for(self, client_id: int, account_id: int, account: Account) -> bool:
        # Verify client + account ID
        self.get_account_for(client_id, account_id)
        if not self.account_dao.update_account_for(client_id, account_id, account):
            raise InvalidParamError("Accounts cannot have a negative balance")
        return True

    def delete_account_for(self, client_id: int, account_id: int) -> bool:
        # Verify client + account ID
        self.get_account_for(client_id, account_id)
        return self.account_dao.delete_account_for(client_id, account_id)

    def update_balance_for(self, client_id: int, account_id: int, change: int) -> bool:
        # Verify client + account ID
        self.get_account_for(client_id, account_id)
        if not self.account_dao.update_balance_for(client_id, account_id, change):
            raise InvalidParamError("Insufficient funds: Try a different amount!")
        return True

    def transfer_funds_to(self, client_id: int, account_from_id: int, account_to_id: int, change: int) -> bool:
        # Verify client ID
        self.get_client(client_id)
        from_account: Account
        try:
            from_account = self.get_account_for(client_id, account_from_id)
        except ResourceNotFoundError:
            raise ResourceNotFoundError("Transfer from account ID invalid")

        to_account: Account
        try:
            to_account = self.get_account_for(client_id, account_to_id)
        except ResourceNotFoundError:
            raise ResourceNotFoundError("Transfer to account ID invalid")

        try:
            self.update_balance_for(client_id, from_account.get_id(), -change)
        except InvalidParamError:
            raise InvalidParamError("Insufficient funds: Try a different amount!")

        try:
            self.update_balance_for(client_id, to_account.get_id(), change)
        except InvalidParamError:
            # Rollback if the second update fails
            self.update_balance_for(client_id, from_account.get_id(), change)
            raise InvalidParamError("Insufficient funds: Try a different amount!")
        return True
