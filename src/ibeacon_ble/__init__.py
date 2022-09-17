from __future__ import annotations

import struct
from dataclasses import dataclass
from uuid import UUID

from home_assistant_bluetooth import BluetoothServiceInfo

UNPACK_IBEACON = struct.Struct(">HHb").unpack

IBEACON_MFR_ID = 76


__version__ = "0.1.0"

__all__ = ["parse", "iBeaconAdvertisement"]


@dataclass
class iBeaconAdvertisement:
    """A dataclass for iBeacon BLE advertisements."""

    uuid: UUID
    major: int
    minor: int
    power: int
    cypress_temperature: float
    cypress_humidity: float
    rssi: int
    source: str


def parse(service_info: BluetoothServiceInfo) -> iBeaconAdvertisement | None:
    if IBEACON_MFR_ID not in service_info.manufacturer_data:
        return None
    data = service_info.manufacturer_data[IBEACON_MFR_ID]

    # Thanks to https://github.com/custom-components/ble_monitor/blob/master/custom_components/ble_monitor/ble_parser/ibeacon.py
    uuid = data[2:18]
    (major, minor, power) = UNPACK_IBEACON(data[18:23])

    return iBeaconAdvertisement(
        uuid=UUID("".join(f"{i:02X}" for i in uuid)),
        major=major,
        minor=minor,
        power=power,
        cypress_temperature=175.72 * ((minor & 0xFF) * 256) / 65536 - 46.85,
        cypress_humidity=125 * ((major & 0xFF) * 256) / 65536 - 6.0,
        rssi=service_info.rssi,
        source=service_info.source,
    )
