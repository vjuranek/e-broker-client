import abc

import sqlite3

from ebroker.Config import Config


def getDb(config_file = None):
    return SQLiteDb(config_file)


class Db(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, config_file = None):
        self._config_file = config_file
        self._connection = None # make sure attribute _connection exists
    
    @abc.abstractmethod
    def connect(self):
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

    def __init__(self, config_file = None):
        super(SQLiteDb, self).__init__(config_file)
        conf = Config(config_file)
        cfg = conf.sqlite_options()
        self._db_file = cfg.db_file
    
    def connect(self):
        self._connection =  sqlite3.connect(self._db_file)

    def execute(self, query, params = None):
        if self._connection is None:
            self.connect()
        if params is None:
            self._connection.execute(query)
        else:
            self._connection.execute(query, params)

    def commit(self):
        self._connection.commit()

    def close(self):
        self._connection.close()


def prepare(db = None):
    _db = db
    if _db is None:
        _db = getDb()
    _db.execute(''' 
    CREATE TABLE requests(ticker int, price double, amount int, symbol varchar(10), amount_satisfied int)
    ''')
    
    
