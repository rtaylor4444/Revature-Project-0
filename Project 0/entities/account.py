class Account:
    def __init__(self, client_id, money: int = 0, account_id: int = 0):
        self.__money = money
        self.__account_id = 0
        self.__owner_id = client_id
        self.set_id(account_id)

    def get_id(self):
        return self.__account_id

    def set_id(self, account_id: int = 0):
        if not self.__account_id == 0:
            return
        self.__account_id = account_id

    def update_amount(self, change: int) -> bool:
        if change < 0 and self.__money + change < 0:
            return False
        self.__money += change
        return True

    def get_amount(self):
        return self.__money

    def get_owner_id(self):
        return self.__owner_id

    def to_dict(self):
        return {
            "Owner": self.__owner_id,
            "Account": self.__account_id,
            "Balance": self.__money
        }
