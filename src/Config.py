import ConfigParser

class Config:

    CREDENTIALS = "CREDENTIALS"
    LOGIN = "login"
    PASSWORD = "password"
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.__config = ConfigParser.ConfigParser()
        self.__config.read(config_file)

    def credentials(self):
        return (self.__config.get(Config.CREDENTIALS,Config.LOGIN), self.__config.get(Config.CREDENTIALS,Config.PASSWORD))
