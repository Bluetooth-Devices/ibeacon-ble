from uuid import UUID

from home_assistant_bluetooth import BluetoothServiceInfo

from ibeacon_ble import iBeaconAdvertisement, parse

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


def test_parse():
    parsed = parse(SERVICE_INFO)
    assert isinstance(parsed, iBeaconAdvertisement)
    assert parsed.cypress_humidity == 118.0234375
    assert parsed.cypress_temperature == 11.494531250000001
    assert parsed.major == 3838
    assert parsed.minor == 4949
    assert parsed.power == -59
    assert parsed.rssi == -60
    assert parsed.uuid == UUID("426c7565-4368-6172-6d42-6561636f6e73")


def test_not_parse():
    parsed = parse(NOT_IBEACON_SERVIE_INFO)
    assert parsed is None
