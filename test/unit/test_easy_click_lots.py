import unittest
import sys

sys.path.append('../..') # TODO anybetter way?

from ebroker.EasyClickLots import EasyClickLots

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.lots  = EasyClickLots()
    
    def test_cez_lots(self):
        cez_lot = self.lots.get_ec_lot(EasyClickLots.CEZ)
        self.assertEqual(cez_lot.lot, 50)

    def test_rounding(self):
        cez_lot = self.lots.get_ec_lot(EasyClickLots.CEZ)
        self.assertEqual(cez_lot.round_lots(80), 50)
        self.assertEqual(cez_lot.round_lots(120), 100)

        
if __name__ == '__main__':
    unittest.main()
