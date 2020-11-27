class Action:
    def __init__(self, command = "", params = [], flags = []):
        self.__command = command
        self.__params = params
        self.__flags = flags

    def get_command(self):
        return self.__command

    def get_params(self):
        return self.__params

    def get_flags(self):
        return self.__flags

class ActionResult:
    def __init__(self, stop = False, error = ""):
        self.__stop = stop
        self.__error = error

    def get_stop(self):
        return self.__stop

    def is_error(self):
        return self.__error != ""

    def get_error(self):
        return self.__error
