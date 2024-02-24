from __future__ import annotations

import asyncio
import contextlib
import struct
from dataclasses import dataclass
from typing import cast
from uuid import UUID

import aiohttp
from home_assistant_bluetooth import BluetoothServiceInfo
from mac_vendor_lookup import AsyncMacLookup

UNPACK_IBEACON = struct.Struct(">HHb").unpack

MAX_THEORETICAL_DISTANCE = 400.0

APPLE_MFR_ID = 76
IBEACON_FIRST_BYTE = 0x02
IBEACON_SECOND_BYTE = 0x15

__version__ = "1.1.0"

__all__ = [
    "parse",
    "is_ibeacon_service_info",
    "iBeaconAdvertisement",
    "APPLE_MFR_ID",
    "IBEACON_FIRST_BYTE",
    "IBEACON_SECOND_BYTE",
]

TILT_UUIDS = {
    "A495BB10C5B14B44B5121370F02D74DE",
    "A495BB20C5B14B44B5121370F02D74DE",
    "A495BB30C5B14B44B5121370F02D74DE",
    "A495BB40C5B14B44B5121370F02D74DE",
    "A495BB50C5B14B44B5121370F02D74DE",
    "A495BB60C5B14B44B5121370F02D74DE",
    "A495BB70C5B14B44B5121370F02D74DE",
    "A495BB80C5B14B44B5121370F02D74DE",
}

BANNED_UUIDS = {"1CA92E23F0874DF7B9A2FD4B716A4BF6"} | TILT_UUIDS


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
    transient: bool
    source: str
    distance: int | None
    vendor: str | None

    def update_rssi(self, rssi: int) -> None:
        """Update the RSSI and distance."""
        self.rssi = rssi
        distance = calculate_distance_meters(self.power, rssi)
        self.distance = int(round(distance)) if distance is not None else None


def is_ibeacon_service_info(service_info: BluetoothServiceInfo) -> bool:
    """Return True if the service info is an iBeacon."""
    if APPLE_MFR_ID not in service_info.manufacturer_data:
        return False
    data = service_info.manufacturer_data[APPLE_MFR_ID]
    if data[0] != IBEACON_FIRST_BYTE or data[1] != IBEACON_SECOND_BYTE:
        return False
    if len(data) < 23:
        return False
    return True


class iBeaconParser:
    """Parse iBeacon BLE advertisements."""

    def __init__(self) -> None:
        """Initialize the parser."""
        self._mac_vendor_lookup: AsyncMacLookup | None = None

    async def async_setup(self) -> None:
        self._mac_vendor_lookup = AsyncMacLookup()
        with contextlib.suppress(asyncio.TimeoutError, aiohttp.ClientError):
            # We don't care if this fails since it only
            # improves the data we get.
            await self._mac_vendor_lookup.load_vendors()

    def _async_get_vendor(self, mac_address: str) -> str | None:
        """Lookup the vendor."""
        assert self._mac_vendor_lookup is not None  # nosec
        oui = self._mac_vendor_lookup.sanitise(mac_address)[:6]
        vendor: bytes | None = self._mac_vendor_lookup.prefixes.get(oui.encode())
        return vendor.decode()[:254] if vendor is not None else None

    def parse(self, service_info: BluetoothServiceInfo) -> iBeaconAdvertisement | None:
        if not is_ibeacon_service_info(service_info):
            return None

        data = service_info.manufacturer_data[APPLE_MFR_ID]
        # Thanks to https://github.com/custom-components/ble_monitor/blob/master/custom_components/ble_monitor/ble_parser/ibeacon.py
        uuid = data[2:18]
        uuid_str = "".join(f"{i:02X}" for i in uuid)

        # Tilt Hydrometers and devices that spew random major/minor values
        # We don't actually need to ban them since the integration will eventually
        # filter them out, but this is a nice optimization.
        if uuid_str in BANNED_UUIDS:
            return None

        name = service_info.name
        transient = False
        if len(name) == 18 and name[0] == "S" and name[17] == "C":
            # If it starts with S and ends with C and the inner
            # 16 characters are hex, it's a random transient
            try:
                int(name[1:17], 16)
                transient = True
            except ValueError:
                pass

        (major, minor, power) = UNPACK_IBEACON(data[18:23])
        distance = calculate_distance_meters(power, service_info.rssi)

        vendor = None
        if ":" in service_info.address:
            vendor = self._async_get_vendor(service_info.address)

        return iBeaconAdvertisement(
            name=service_info.name,
            uuid=UUID(uuid_str),
            major=major,
            minor=minor,
            power=power,
            cypress_temperature=175.72 * ((minor & 0xFF) * 256) / 65536 - 46.85,
            cypress_humidity=125 * ((major & 0xFF) * 256) / 65536 - 6.0,
            rssi=service_info.rssi,
            source=service_info.source,
            transient=transient,
            vendor=vendor,
            distance=int(round(distance)) if distance is not None else None,
        )


def calculate_distance_meters(power: int, rssi: int) -> float | None:
    """Calculate the distance in meters between the device and the beacon."""
    if rssi == 0 or power == 0:
        return None
    if (ratio := rssi * 1.0 / power) < 1.0:
        distance = pow(ratio, 10)
    else:
        distance = cast(float, 0.89976 * pow(ratio, 7.7095) + 0.111)
    return min(distance, MAX_THEORETICAL_DISTANCE)
