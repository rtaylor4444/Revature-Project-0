from daos.client_dao_base import ClientDAOBase
from daos.client_dao_local import ClientDAOLocal
from daos.client_dao_postgres import ClientDAOPostgres
from entities.client import Client
from unittest import TestCase

#client_dao: ClientDAOBase = ClientDAOLocal()
client_dao: ClientDAOBase = ClientDAOPostgres()


def test_post_client():
    client: Client = Client("Client1")
    assert client_dao.post_client(client)


def test_post_client_invalid():
    client: Client = Client("")
    assert not client_dao.post_client(client)


def test_get_client_pass():
    client: Client = Client("Client2")
    client_dao.post_client(client)
    result: Client = client_dao.get_client(client.get_id())
    TestCase().assertDictEqual(result.to_dict(), client.to_dict())


def test_get_client_fail():
    assert client_dao.get_client(-1) is None


def test_get_clients():
    client_list = client_dao.get_clients()
    TestCase().assertDictEqual({"Name": client_list[0].get_name(),
                                "ID": client_list[0].get_id()},
                               client_list[0].to_dict())
    TestCase().assertDictEqual({"Name": client_list[1].get_name(),
                                "ID": client_list[1].get_id()},
                               client_list[1].to_dict())


def test_update_client():
    client_old: Client = Client("Client3")
    client_dao.post_client(client_old)
    client_new: Client = Client("Client3new")
    assert client_dao.update_client(client_old.get_id(), client_new)
    client_old = client_dao.get_client(client_new.get_id())
    TestCase().assertDictEqual(client_old.to_dict(), client_new.to_dict())


def test_update_client_fail():
    client: Client = Client("Client3")
    client_dao.post_client(client)
    assert not client_dao.update_client(-1, client)


def test_update_client_invalid():
    client_old: Client = Client("Client3")
    client_dao.post_client(client_old)
    client_new: Client = Client("")
    assert not client_dao.update_client(client_old.get_id(), client_new)


def test_remove_client():
    client: Client = Client("Client4")
    client_dao.post_client(client)
    assert client_dao.remove_client(client.get_id())
    assert not client_dao.remove_client(-1)
