from uuid import UUID

import pytest
from home_assistant_bluetooth import BluetoothServiceInfo

from ibeacon_ble import calculate_distance_meters, iBeaconAdvertisement, iBeaconParser

pytestmark = pytest.mark.asyncio

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
TESLA_TRANSIENT = BluetoothServiceInfo(
    address="00:00:00:00:00:00",
    rssi=-60,
    name="S6da7c9389bd5452cC",
    manufacturer_data={
        76: b"\x02\x15t'\x8b\xda\xb6DE \x8f\x0cr\x0e\xaf\x05\x995\x00\x00[$\xc5"
    },
    service_data={},
    service_uuids=[],
    source="hci0",
)
SC_NOT_RANDOM_TRANSIENT = BluetoothServiceInfo(
    address="00:00:00:00:00:00",
    rssi=-60,
    name="SISAHAPPYPERSONINC",
    manufacturer_data={
        76: b"\x02\x15t'\x8b\xda\xb6DE \x8f\x0cr\x0e\xaf\x05\x995\x00\x00[$\xc5"
    },
    service_data={},
    service_uuids=[],
    source="hci0",
)
TELINK_VENDOR = BluetoothServiceInfo(
    address="A4:C1:38:12:D6:FB",
    rssi=-60,
    name="gvh423",
    manufacturer_data={
        76: b"\x02\x15t'\x8b\xda\xb6DE \x8f\x0cr\x0e\xaf\x05\x995\x00\x00[$\xc5"
    },
    service_data={},
    service_uuids=[],
    source="hci0",
)


async def test_parse():
    ibeacon = iBeaconParser()
    await ibeacon.async_setup()
    parsed = ibeacon.parse(SERVICE_INFO)
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
    assert parsed.distance == 3


async def test_not_parse():
    ibeacon = iBeaconParser()
    await ibeacon.async_setup()
    parsed = ibeacon.parse(NOT_IBEACON_SERVIE_INFO)
    assert parsed is None


async def test_not_parse_2():
    ibeacon = iBeaconParser()
    await ibeacon.async_setup()
    parsed = ibeacon.parse(NOT_IBEACON_SERVIE_INFO_2)
    assert parsed is None


async def test_not_parse_short_service_info():
    ibeacon = iBeaconParser()
    await ibeacon.async_setup()
    parsed = ibeacon.parse(SHORT_SERVICE_INFO)
    assert parsed is None


async def test_ignore_tilt():
    ibeacon = iBeaconParser()
    await ibeacon.async_setup()
    parsed = ibeacon.parse(TILT_SERVICE_INFO)
    assert parsed is None


async def test_telsa_transient():
    ibeacon = iBeaconParser()
    await ibeacon.async_setup()
    parsed = ibeacon.parse(TESLA_TRANSIENT)
    assert parsed is not None
    assert parsed.transient is True


async def test_not_random_transient():
    ibeacon = iBeaconParser()
    await ibeacon.async_setup()
    parsed = ibeacon.parse(SC_NOT_RANDOM_TRANSIENT)
    assert parsed is not None


async def test_ibeacon_zero_power():
    ibeacon = iBeaconParser()
    await ibeacon.async_setup()
    parsed = ibeacon.parse(IBEACON_ZERO_POWER)
    assert parsed is not None
    assert parsed.distance is None


async def test_vendor():
    ibeacon = iBeaconParser()
    await ibeacon.async_setup()
    parsed = ibeacon.parse(TELINK_VENDOR)
    assert parsed is not None
    assert parsed.vendor == "Telink Semiconductor (Taipei) Co. Ltd."


def tests_calculate_distance_meters():
    assert calculate_distance_meters(-59, -60) == 1.1352362990362899
    assert calculate_distance_meters(59, -60) == 1.183020818815412
    assert calculate_distance_meters(12, -80) == 400.0
    assert calculate_distance_meters(59, 0) is None
    assert calculate_distance_meters(-3, -100) == 400.0
    assert calculate_distance_meters(-3, -96) == 400.0
    assert calculate_distance_meters(-3, -3) == 1.01076
    assert calculate_distance_meters(-4, -3) == 0.056313514709472656
