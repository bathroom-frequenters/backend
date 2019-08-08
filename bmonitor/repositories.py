from django.utils import timezone
from influxdb import InfluxDBClient
from influxdb.resultset import ResultSet
from typing import List

from .entities import AvailabilityRecord

from api.utils import get_influxdb_client


def create_availability(available: bool) -> bool:
    client: InfluxDBClient = get_influxdb_client()

    point = {
        "measurement": "available",
        "fields": {"value": available},
        "timestamp": timezone.localtime().isoformat("T"),
    }

    return client.write_points([point])


def get_latest_availability() -> AvailabilityRecord:
    client: InfluxDBClient = get_influxdb_client()

    result: ResultSet = client.query(
        "SELECT time, LAST(value) as available FROM available LIMIT 1"
    )

    point, *_ = list(result.get_points())

    return AvailabilityRecord(**point)


def get_recent_availability() -> List[AvailabilityRecord]:
    client: InfluxDBClient = get_influxdb_client()
    result: ResultSet = client.query(
        "SELECT time, max(value) as available FROM available WHERE time > now() - 1h GROUP BY time(1m) FILL(previous)"
    )

    return list(map(lambda point: AvailabilityRecord(**point), result.get_points()))
