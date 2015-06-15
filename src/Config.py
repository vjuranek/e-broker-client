import os
import collections
import ConfigParser

Credentials = collections.namedtuple("Credentials", "login password")

class Config:

    CREDENTIALS = "CREDENTIALS"
    LOGIN = "login"
    PASSWORD = "password"
    
    def __init__(self, config_file = None):
        if config_file is None:
            home_dir = os.path.expanduser("~")
            self.config_file = os.path.join(home_dir, ".ebroker", "main.conf")
        else:    
            self.config_file = config_file
        self.__config = ConfigParser.ConfigParser()
        self.__config.read(self.config_file)

    def credentials(self):
        return Credentials(self.__config.get(Config.CREDENTIALS,Config.LOGIN), self.__config.get(Config.CREDENTIALS,Config.PASSWORD))
