from uuid import UUID

from home_assistant_bluetooth import BluetoothServiceInfo

from ibeacon_ble import calculate_distance_meters, iBeaconAdvertisement, parse

SERVICE_INFO = BluetoothServiceInfo(
    address="00:00:00:00:00:00",
    rssi=-60,
    name="BlueCharm_177999",
    manufacturer_data={76: b"\x02\x15BlueCharmBeacons\x0e\xfe\x13U\xc5"},
    service_data={
        "00002080-0000-1000-8000-00805f9b34fb": b"k\x0c\x0e\xfe\x13U",
        "0000feaa-0000-1000-8000-00805f9b34fb": b" \x00\x0b\xfe\x1c\x00\x00\x00\x07\x08\x00\x00>|",
    },
    service_uuids=["0000feaa-0000-1000-8000-00805f9b34fb"],
    source="hci0",
)
NOT_IBEACON_SERVIE_INFO = BluetoothServiceInfo(
    address="00:00:00:00:00:00",
    rssi=-60,
    name="not",
    manufacturer_data={21: b"\x02\x15BlueCharmBeacons\x0e\xfe\x13U\xc5"},
    service_data={},
    service_uuids=[],
    source="hci0",
)
NOT_IBEACON_SERVIE_INFO_2 = BluetoothServiceInfo(
    address="00:00:00:00:00:00",
    rssi=-60,
    name="not",
    manufacturer_data={76: b"\x10\x15BlueCharmBeacons\x0e\xfe\x13U\xc5"},
    service_data={},
    service_uuids=[],
    source="hci0",
)


def test_parse():
    parsed = parse(SERVICE_INFO)
    assert isinstance(parsed, iBeaconAdvertisement)
    assert parsed.cypress_humidity == 118.0234375
    assert parsed.cypress_temperature == 11.494531250000001
    assert parsed.major == 3838
    assert parsed.minor == 4949
    assert parsed.power == -59
    assert parsed.rssi == -60
    assert parsed.distance == 1.1
    assert parsed.uuid == UUID("426c7565-4368-6172-6d42-6561636f6e73")


def test_not_parse():
    parsed = parse(NOT_IBEACON_SERVIE_INFO)
    assert parsed is None


def test_not_parse_2():
    parsed = parse(NOT_IBEACON_SERVIE_INFO_2)
    assert parsed is None


def tests_calculate_distance_meters():
    assert calculate_distance_meters(-59, -60) == 1.1352362990362899
    assert calculate_distance_meters(59, -60) == 1.183020818815412
    assert calculate_distance_meters(59, 0) is None
    assert calculate_distance_meters(-3, -100) is None
    assert calculate_distance_meters(-3, -3) == 1.01076
    assert calculate_distance_meters(-4, -3) == 0.056313514709472656
