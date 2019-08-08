from dataclasses import dataclass


@dataclass(frozen=True)
class AvailabilityRecord:
    available: bool
    # RFC 3339 timestamp
    time: str
