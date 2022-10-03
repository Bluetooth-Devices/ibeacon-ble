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

SHORT_SERVICE_INFO = BluetoothServiceInfo(
    address="00:00:00:00:00:00",
    rssi=-60,
    name="not",
    manufacturer_data={76: b"\x02\x15BlueCharmBeacons"},
    service_data={},
    service_uuids=[],
    source="hci0",
)

TILT_SERVICE_INFO = BluetoothServiceInfo(
    address="00:00:00:00:00:00",
    rssi=-60,
    name="tilt",
    manufacturer_data={
        76: b"\x02\x15\xa4\x95\xbbp\xc5\xb1KD\xb5\x12\x13p\xf0-t\xde\x00X\x06\xc8\xc5"
    },
    service_data={},
    service_uuids=[],
    source="hci0",
)
IBEACON_ZERO_POWER = BluetoothServiceInfo(
    address="00:00:00:00:00:00",
    rssi=-60,
    name="not",
    manufacturer_data={76: b"\x02\x15BlueCharmBeacons\x0e\xfe\x13U\x00"},
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
    assert parsed.distance == 1
    assert parsed.uuid == UUID("426c7565-4368-6172-6d42-6561636f6e73")

    parsed.update_rssi(-70)
    assert parsed.rssi == -70
    assert parsed.distance == 4


def test_not_parse():
    parsed = parse(NOT_IBEACON_SERVIE_INFO)
    assert parsed is None


def test_not_parse_2():
    parsed = parse(NOT_IBEACON_SERVIE_INFO_2)
    assert parsed is None


def test_not_parse_short_service_info():
    parsed = parse(SHORT_SERVICE_INFO)
    assert parsed is None


def test_ignore_tilt():
    parsed = parse(TILT_SERVICE_INFO)
    assert parsed is None


def test_ibeacon_zero_power():
    parsed = parse(IBEACON_ZERO_POWER)
    assert parsed is not None
    assert parsed.distance is None


def tests_calculate_distance_meters():
    assert calculate_distance_meters(-59, -60) == 1.1220184543019636
    assert calculate_distance_meters(59, -60) == 400.0
    assert calculate_distance_meters(12, -80) == 400.0
    assert calculate_distance_meters(59, 0) is None
    assert calculate_distance_meters(-3, -100) == 400.0
    assert calculate_distance_meters(-3, -96) == 400.0
    assert calculate_distance_meters(-3, -3) == 1
    assert calculate_distance_meters(-4, -3) == 0.8912509381337456
    assert calculate_distance_meters(-40, -66) == 19.952623149688797
    assert calculate_distance_meters(-40, -46) == 1.9952623149688795
