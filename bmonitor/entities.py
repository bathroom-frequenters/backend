from dataclasses import dataclass


@dataclass(frozen=True)
class AvailabilityRecord:
    __slots__ = ["available", "time"]

    available: bool
    # RFC 3339 timestamp
    time: str
