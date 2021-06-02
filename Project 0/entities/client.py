

class Client:

    def __init__(self, name: str = "") -> None:
        self.__client_id = 0
        self.__name = name

    def get_id(self) -> int:
        return self.__client_id

    def set_id(self, client_id: int = 0) -> None:
        if not self.__client_id == 0:
            return
        self.__client_id = client_id

    def get_name(self) -> str:
        return self.__name

    def to_dict(self) -> {}:
        return {
            "Name": self.__name,
            "ID": self.__client_id
        }
