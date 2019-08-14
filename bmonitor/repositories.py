from datetime import timedelta, datetime
from django.utils import timezone
from influxdb import InfluxDBClient
from influxdb.resultset import ResultSet
from typing import List

from .entities import AvailabilityRecord

from api.utils import get_influxdb_client


def create_availability(available: bool) -> bool:
    client: InfluxDBClient = get_influxdb_client()

    point = {"measurement": "available", "fields": {"value": available}}

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
        "SELECT time, last(value) as available FROM available WHERE time > now() - 1h GROUP BY time(1m) FILL(previous)"
    )

    records = list(map(lambda point: AvailabilityRecord(**point), result.get_points()))

    # reverse the records because they are returned in ascending order and we want descending
    #  UNFORTUNATELY InfluxDB screws up the results when you try `ORDER BY time DESC`
    records = list(reversed(records))

    if len(records) > 0:
        # Check for null-record pollution when data falls out of query scope
        if records[0].available is None:
            pass

    else:
        # There are no records for the previous 60 minutes, have to find the last one, and build an
        #  array for the past 60 minutes from its value
        def calc_timestamp(minutes_ago: int) -> str:
            timestamp: datetime = timezone.localtime()
            timestamp = timestamp.replace(minute=0)
            timestamp -= timedelta(minutes=minutes_ago)

            return timestamp.isoformat("T")

        records = []

        try:
            last_seen = get_latest_availability()
        except:
            # In case get_latest_availability() returns no results, return an empty array
            pass
        else:
            for minute in range(60):
                records.append(
                    AvailabilityRecord(
                        available=last_seen.available, time=calc_timestamp(minute)
                    )
                )

    return records
