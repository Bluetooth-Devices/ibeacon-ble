from ibeacon_ble import iBeaconAdvertisement, parse


def test_parse():
    isinstance(parse(), iBeaconAdvertisement)
