from ebroker.EasyClickLots import EasyClickLots


def test_cez_lots():
    lots = EasyClickLots()
    cez_lot = lots.get_ec_lot(EasyClickLots.CEZ)
    cez_lot.lot == 50


def test_rounding():
    lots = EasyClickLots()
    cez_lot = lots.get_ec_lot(EasyClickLots.CEZ)
    cez_lot.round_lots(80) == 50
    cez_lot.round_lots(120) == 100
