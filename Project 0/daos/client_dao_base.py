from abc import ABC, abstractmethod
from typing import List
from entities.client import Client


class ClientDAOBase(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

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

