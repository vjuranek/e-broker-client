import abc

import sqlite3

import Config

class Db(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._connection = self.connect()
    
    @abc.abstractmethod
    def connect(self, config_file = None):
        raise NotImplementedError("Called method is not implemented")

    @abc.abstractmethod
    def execute(self, query, params = None):
        raise NotImplementedError("Called method is not implemented")

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError("Called method is not implemented")

    @abc.abstractmethod
    def close(self):
        raise NotImplementedError("Called method is not implemented")
    


class SQLiteDb(Db):
    def connect(self, config_file):
        conf = Config(config_file)
        cfg = conf.sqlite_options()
        sqlite3.connect(cfg.db_file)

    def execute(self, query, params = None):
        self._connection.execute(query, params)

    def commit(self):
        self._connection.commit()

    def close(self):
        self._connection.close()
