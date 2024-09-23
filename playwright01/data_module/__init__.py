import time


class As_dict:
    def as_dict(self):
        # return_dict = self.__dict__
        # temp_dict = self.__dict__().copy()
        # for key, value in temp_dict.items():
        #     if value == "":
        #         return_dict.pop(key)
        #         continue
        #     if "time" in value:
        #         value = str(value).replace('time', str(time.time_ns()))
        #         return_dict.update({key: value})
        #
        # return return_dict
        return_dict = self.__dict__
        temp_dict = self.__dict__.copy()
        for key, value in temp_dict.items():
            if "time" in value:
                value = str(value).replace('time', str(time.time_ns()))
                return_dict.update({key: value})
        return return_dict