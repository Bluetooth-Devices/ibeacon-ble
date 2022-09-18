from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import cast
from uuid import UUID

from home_assistant_bluetooth import BluetoothServiceInfo

UNPACK_IBEACON = struct.Struct(">HHb").unpack


APPLE_MFR_ID = 76
IBEACON_FIRST_BYTE = 0x02
IBEACON_SECOND_BYTE = 0x15

__version__ = "0.5.0"

__all__ = [
    "parse",
    "is_ibeacon_service_info",
    "iBeaconAdvertisement",
]


@dataclass
class iBeaconAdvertisement:
    """A dataclass for iBeacon BLE advertisements."""

    name: str
    uuid: UUID
    major: int
    minor: int
    power: int
    cypress_temperature: float
    cypress_humidity: float
    rssi: int
    source: str
    distance: float | None


def is_ibeacon_service_info(service_info: BluetoothServiceInfo) -> bool:
    """Return True if the service info is an iBeacon."""
    if APPLE_MFR_ID not in service_info.manufacturer_data:
        return False
    data = service_info.manufacturer_data[APPLE_MFR_ID]
    if data[0] != IBEACON_FIRST_BYTE or data[1] != IBEACON_SECOND_BYTE:
        return False
    return True


def parse(service_info: BluetoothServiceInfo) -> iBeaconAdvertisement | None:
    if not is_ibeacon_service_info(service_info):
        return None

    data = service_info.manufacturer_data[APPLE_MFR_ID]

    # Thanks to https://github.com/custom-components/ble_monitor/blob/master/custom_components/ble_monitor/ble_parser/ibeacon.py
    uuid = data[2:18]
    (major, minor, power) = UNPACK_IBEACON(data[18:23])

    return iBeaconAdvertisement(
        name=service_info.name,
        uuid=UUID("".join(f"{i:02X}" for i in uuid)),
        major=major,
        minor=minor,
        power=power,
        cypress_temperature=175.72 * ((minor & 0xFF) * 256) / 65536 - 46.85,
        cypress_humidity=125 * ((major & 0xFF) * 256) / 65536 - 6.0,
        rssi=service_info.rssi,
        source=service_info.source,
        distance=calculate_distance_meters(power, service_info.rssi),
    )


def calculate_distance_meters(power: int, rssi: int) -> float | None:
    """Calculate the distance in meters between the device and the beacon."""
    if rssi == 0:
        return None
    if (ratio := rssi * 1.0 / power) < 1.0:
        return pow(ratio, 10)
    distance = cast(float, 0.89976 * pow(ratio, 7.7095) + 0.111)
    return distance if distance < 1000 else None
