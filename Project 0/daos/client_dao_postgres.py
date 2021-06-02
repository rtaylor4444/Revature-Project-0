from typing import List
from daos.client_dao_base import ClientDAOBase
from entities.client import Client
from utils.connection_util import connection


class ClientDAOPostgres(ClientDAOBase):
    def __init__(self) -> None:
        pass

    def post_client(self, client: Client) -> bool:
        if 3 > len(client.get_name()) or len(client.get_name()) > 50:
            return False

        sql = """insert into client (client_name) values (%s) returning client_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (client.get_name(),))
        connection.commit()
        client.set_id(cursor.fetchone()[0])
        return True

    def get_client(self, client_id: int) -> Client:
        sql = """select * from client where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        record = cursor.fetchone()
        if record is None:
            return None

        client = Client(record[1])
        client.set_id(record[0])
        return client

    def get_clients(self) -> List[Client]:
        sql = """select * from client"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        client_list: List[Client] = []
        for record in records:
            client: Client = Client(record[1])
            client.set_id(record[0])
            client_list.append(client)

        return client_list

    def update_client(self, client_id: int, client: Client) -> bool:
        if 3 > len(client.get_name()) or len(client.get_name()) > 50:
            return False

        sql = """update client set client_name=%s where client_id =%s"""
        cursor = connection.cursor()
        cursor.execute(sql, [client.get_name(), client_id])
        connection.commit()

        # Verify record is updated
        updated_client = self.get_client(client_id)
        if updated_client is None or updated_client.get_name() != client.get_name():
            return False

        client.set_id(client_id)
        return True

    def remove_client(self, client_id: int) -> bool:
        # Verify record exists
        if self.get_client(client_id) is None:
            return False

        sql = """delete from client where client_id =%s"""
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        connection.commit()
        return True
