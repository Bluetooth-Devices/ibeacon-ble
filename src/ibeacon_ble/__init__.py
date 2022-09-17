__version__ = "0.0.1"
from dataclasses import dataclass

__all__ = ["parse", "IBeaconAdvertisement"]


@dataclass
class IBeaconAdvertisement:
    """A dataclass for iBeacon BLE advertisements."""

    uuid: str
    major: int
    minor: int
    power: int


def parse() -> IBeaconAdvertisement:
    return IBeaconAdvertisement(
        uuid="00000000-0000-0000-0000-000000000000",
        major=0,
        minor=0,
        power=0,
    )
