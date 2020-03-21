import os
import collections
import configparser

Credentials = collections.namedtuple("Credentials", "login password")
SQLiteConf = collections.namedtuple("SQLiteConf", "db_file")


class Config:

    CREDENTIALS = "CREDENTIALS"
    LOGIN = "login"
    PASSWORD = "password"

    DB = "DB"
    SQLITE_FILE = "sqlite_file"

    def __init__(self, config_file=None):
        if config_file is None:
            home_dir = os.path.expanduser("~")
            self.config_file = os.path.join(home_dir, ".ebroker", "main.conf")
        else:
            self.config_file = config_file
        self.__config = configparser.ConfigParser()
        self.__config.read(self.config_file)

    def credentials(self):
        return Credentials(
            self.__config.get(Config.CREDENTIALS, Config.LOGIN),
            self.__config.get(Config.CREDENTIALS, Config.PASSWORD))

    def sqlite_options(self):
        return SQLiteConf(self.__config.get(Config.DB, Config.SQLITE_FILE))
