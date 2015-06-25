import unittest
import os, sys

sys.path.append('../..') # TODO anybetter way?

from ebroker.Config import Config, Credentials

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config = Config(os.path.join(os.path.dirname(__file__), "..", "resources", "main.conf"))
    
    def test_credentials(self):
        cred = self.config.credentials()
        self.assertEqual(cred.login, 'test_login')
        self.assertEqual(cred.password, 'test_password')


    def test_db_config(self):
        sqlite_conf = self.config.sqlite_options()
        self.assertEqual(sqlite_conf.db_file, "test_location")
        
        
if __name__ == '__main__':
    unittest.main()
