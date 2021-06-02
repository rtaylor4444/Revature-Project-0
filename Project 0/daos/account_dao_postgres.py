from typing import List
from daos.account_dao_base import AccountDAOBase
from entities.account import Account
from utils.connection_util import connection


class AccountDAOPostgres(AccountDAOBase):
    def __init__(self) -> None:
        pass

    def remove_client_dict(self, client_id: int) -> bool:
        pass

    def post_new_account_for(self, client_id: int, account: Account) -> bool:
        if account.get_amount() < 0:
            return False

        sql = """insert into account (amount, client_id) values (%s, %s) returning account_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (account.get_amount(), client_id))
        connection.commit()
        account.set_id(cursor.fetchone()[0])
        return True

    def get_all_accounts_for(self, client_id: int) -> List[Account]:
        sql = """select * from account where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (client_id,))
        records = cursor.fetchall()
        account_list: List[Account] = []
        for record in records:
            account_list.append(Account(record[2], record[1], record[0]))

        return account_list

    def get_account_for(self, client_id: int, account_id: int) -> Account:
        sql = """select * from account where account_id = %s and client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [account_id, client_id])
        record = cursor.fetchone()
        if record is None:
            return None

        account: Account = Account(record[2], record[1])
        account.set_id(record[0])
        return account

    def update_account_for(self, client_id: int, account_id: int, account: Account) -> bool:
        if account.get_amount() < 0:
            return False

        sql = """update account set amount=%s where account_id = %s and client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [account.get_amount(), account_id, client_id])
        connection.commit()

        # Verify record is updated
        updated_account: Account = self.get_account_for(client_id, account_id)
        if updated_account is None or updated_account.get_amount() != account.get_amount():
            return False

        account.set_id(account_id)
        return True

    def delete_account_for(self, client_id: int, account_id: int) -> bool:
        if self.get_account_for(client_id, account_id) is None:
            return False

        sql = """delete from account where account_id = %s and client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [account_id, client_id])
        connection.commit()
        return True

    def update_balance_for(self, client_id: int, account_id: int, change: int) -> bool:
        account: Account = self.get_account_for(client_id, account_id)
        if account is None or not account.update_amount(change):
            return False

        return self.update_account_for(client_id, account_id, account)
