#class used to manage our local cache
class IdDictionary:
    def __init__(self):
        self.__available_ids = []
        self.__data = {}

    def verify_data(self, index: int) -> bool:
        return index in self.__data

    def insert_data(self, data) -> None:
        # If there a no freed ids make a new one for use
        if len(self.__available_ids) == 0:
            self.__available_ids.append(len(self.__data)+1)

        #Assign this id to the object if the method is defined
        new_id: int = self.__available_ids[0]
        if hasattr(data, "set_id"):
            data.set_id(new_id)

        self.__available_ids.pop(0)
        self.__data.update({new_id: data})

    def get_all_data(self) -> []:
        data_list = []
        for key in self.__data.keys():
            data_list.append(self.__data[key])
        return data_list

    def get_data(self, index: int):
        if not self.verify_data(index):
            return None

        return self.__data[index]

    def update_data(self, index: int, data) -> bool:
        if not self.verify_data(index):
            return False

        self.__data[index] = data
        return True

    def remove_data(self, index: int) -> bool:
        if not self.verify_data(index):
            return False

        self.__data.pop(index)
        #Add removed id for future reuse
        self.__available_ids.append(index)
        return True
