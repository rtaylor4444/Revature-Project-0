import math
from flask import request, jsonify
from typing import List
from services.client_service import ClientService
from daos.client_dao_local import ClientDAOLocal
from daos.client_dao_postgres import ClientDAOPostgres
from daos.account_dao_local import AccountDAOLocal
from daos.account_dao_postgres import AccountDAOPostgres
from entities.client import Client
from entities.account import Account
from exceptions.invalid_param_exception import InvalidParamError
from exceptions.not_found_exception import ResourceNotFoundError


class RouteManager:
    def __init__(self):
        self.__client_service = ClientService(ClientDAOPostgres(), AccountDAOPostgres())

    def get_id_from_string(self, type_id: str):
        if not type_id.isdigit():
            return -1
        else:
            return int(type_id)

    def post_client(self):
        body = request.json
        try:
            client: Client = Client(body["Name"])
            self.__client_service.post_client(client)
            return jsonify(client.to_dict()), 201
        except KeyError:
            return "No data was entered check your spelling", 400
        except InvalidParamError as e:
            return e.message, 400

    def get_clients(self):
        clients: List[Client] = self.__client_service.get_clients()
        json_clients = [c.to_dict() for c in clients]
        return jsonify(json_clients), 200

    def get_client(self, client_id: str):
        converted_id: int = self.get_id_from_string(client_id)
        try:
            client: Client = self.__client_service.get_client(converted_id)
            return jsonify(client.to_dict()), 200
        except ResourceNotFoundError as e:
            return e.message, 404

    def update_client(self, client_id: str):
        body = request.json
        converted_id: int = self.get_id_from_string(client_id)
        try:
            client: Client = Client(body["Name"])
            self.__client_service.update_client(converted_id, client)
            return jsonify(client.to_dict()), 200
        except KeyError:
            return "No data was entered check your spelling", 400
        except ResourceNotFoundError as e:
            return e.message, 404
        except InvalidParamError as e:
            return e.message, 400

    def remove_client(self, client_id: str):
        converted_id: int = self.get_id_from_string(client_id)
        try:
            self.__client_service.remove_client(converted_id)
            return "Successfully removed Client", 205
        except ResourceNotFoundError as e:
            return e.message, 404

    def post_new_account_for(self, client_id: str):
        body = request.json
        converted_id: int = self.get_id_from_string(client_id)
        try:
            account: Account = Account(converted_id, body["Balance"])
            self.__client_service.post_new_account_for(converted_id, account)
            return jsonify(account.to_dict()), 201
        except KeyError:
            return "No data was entered check your spelling", 400
        except ResourceNotFoundError as e:
            return e.message, 404
        except InvalidParamError as e:
            return e.message, 400

    def get_all_accounts_for(self, client_id: str):
        converted_id: int = self.get_id_from_string(client_id)
        amount_less_than = request.args.get("amountLessThan")
        amount_greater_than = request.args.get("amountGreaterThan")
        less_than = math.inf
        greater_than: int = -1
        if amount_less_than is not None:
            less_than = self.get_id_from_string(str(amount_less_than))
            if less_than == -1:
                less_than = math.inf
        if amount_greater_than is not None:
            greater_than = self.get_id_from_string(str(amount_greater_than))

        try:
            accounts: List[Account]
            accounts = self.__client_service.get_all_accounts_for(converted_id,
                                                                  less_than, greater_than)
            json_accounts = [a.to_dict() for a in accounts]
            return jsonify(json_accounts), 200
        except ResourceNotFoundError as e:
            return e.message, 404

    def get_account_for(self, client_id: str, account_id: str):
        new_client_id: int = self.get_id_from_string(client_id)
        new_account_id: int = self.get_id_from_string(account_id)
        try:
            account: Account = self.__client_service.get_account_for(new_client_id, new_account_id)
            return jsonify(account.to_dict()), 200
        except ResourceNotFoundError as e:
            return e.message, 404

    def update_account_for(self, client_id: str, account_id: str):
        new_client_id: int = self.get_id_from_string(client_id)
        new_account_id: int = self.get_id_from_string(account_id)
        try:
            body = request.json
            account: Account = Account(new_client_id, body["Balance"])
            self.__client_service.update_account_for(new_client_id, new_account_id, account)
            return jsonify(account.to_dict()), 200
        except KeyError:
            return "No data was entered check your spelling", 400
        except ResourceNotFoundError as e:
            return e.message, 404
        except InvalidParamError as e:
            return e.message, 400

    def delete_account_for(self, client_id: str, account_id: str):
        new_client_id: int = self.get_id_from_string(client_id)
        new_account_id: int = self.get_id_from_string(account_id)
        try:
            self.__client_service.delete_account_for(new_client_id, new_account_id)
            return "Successfully removed Account", 205
        except ResourceNotFoundError as e:
            return e.message, 404

    def update_balance_for(self, client_id: str, account_id: str):
        new_client_id: int = self.get_id_from_string(client_id)
        new_account_id: int = self.get_id_from_string(account_id)
        body = request.json
        change: int = 0
        if body.get("withdraw") is None and body.get("deposit") is None:
            return "No data was entered check your spelling", 400
        if body.get("withdraw") is not None:
            change -= body["withdraw"]
        if body.get("deposit") is not None:
            change += body["deposit"]

        try:
            self.__client_service.update_balance_for(new_client_id, new_account_id, change)
            account: Account = self.__client_service.get_account_for(new_client_id, new_account_id)
            return jsonify(account.to_dict()), 200
        except ResourceNotFoundError as e:
            return e.message, 404
        except InvalidParamError as e:
            return e.message, 422

    def transfer_funds_to(self, client_id: str, account_from_id: str, account_to_id: str):
        new_client_id: int = self.get_id_from_string(client_id)
        new_account_from_id: int = self.get_id_from_string(account_from_id)
        new_account_to_id: int = self.get_id_from_string(account_to_id)
        body = request.json
        try:
            self.__client_service.transfer_funds_to(new_client_id, new_account_from_id,
                                                    new_account_to_id, body["amount"])
            accounts: List[Account] = [self.__client_service.get_account_for(new_client_id, new_account_from_id),
                                       self.__client_service.get_account_for(new_client_id, new_account_to_id)]
            json_accounts = [a.to_dict() for a in accounts]
            return jsonify(json_accounts), 200
        except KeyError:
            return "No data was entered check your spelling", 400
        except ResourceNotFoundError as e:
            return e.message, 404
        except InvalidParamError as e:
            return e.message, 422
