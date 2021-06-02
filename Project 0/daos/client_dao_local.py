from daos.id_dictionary import IdDictionary
from daos.client_dao_base import ClientDAOBase
from typing import List
from entities.client import Client


class ClientDAOLocal(ClientDAOBase):
    def __init__(self):
        self.__localCache = IdDictionary()

    def post_client(self, client: Client) -> bool:
        if len(client.get_name()) < 3:
            return False

        self.__localCache.insert_data(client)
        return True

    def get_client(self, client_id: int) -> Client:
        return self.__localCache.get_data(client_id)

    def get_clients(self) -> List[Client]:
        return self.__localCache.get_all_data()

    def update_client(self, client_id: int, client: Client) -> bool:
        if len(client.get_name()) < 3:
            return False

        if self.__localCache.update_data(client_id, client):
            client.set_id(client_id)
            return True
        else:
            return False

    def remove_client(self, client_id: int) -> bool:
        return self.__localCache.remove_data(client_id)
