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

        
if __name__ == '__main__':
    unittest.main()
