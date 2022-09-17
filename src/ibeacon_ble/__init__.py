__version__ = "0.1.0"
from dataclasses import dataclass

__all__ = ["parse", "iBeaconAdvertisement"]


@dataclass
class iBeaconAdvertisement:
    """A dataclass for iBeacon BLE advertisements."""

    uuid: str
    major: int
    minor: int
    power: int


def parse() -> iBeaconAdvertisement:
    return iBeaconAdvertisement(
        uuid="00000000-0000-0000-0000-000000000000",
        major=0,
        minor=0,
        power=0,
    )
