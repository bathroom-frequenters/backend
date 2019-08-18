from dataclasses import asdict
from datetime import timedelta, datetime
from django.utils import timezone
from influxdb import InfluxDBClient
from influxdb.resultset import ResultSet
from typing import List, Optional

from .entities import AvailabilityRecord

from api.utils import get_influxdb_client


def _get_points(client: InfluxDBClient, query: str) -> List[AvailabilityRecord]:
    result: ResultSet = client.query(query)
    records: List[AvailabilityRecord] = list(
        map(lambda point: AvailabilityRecord(**point), result.get_points())
    )
    return records


def create_availability(available: bool) -> bool:
    client: InfluxDBClient = get_influxdb_client()

    point = {"measurement": "available", "fields": {"value": available}}

    return client.write_points([point])


def get_latest_availability(
    client: Optional[InfluxDBClient] = None
) -> AvailabilityRecord:
    client = client or get_influxdb_client()

    try:
        point, *_ = _get_points(
            client, "SELECT time, LAST(value) as available FROM available LIMIT 1"
        )
    except:
        # TODO refactor to support returning no data
        return AvailabilityRecord(False, "")
    else:
        return point


def get_recent_availability(
    client: Optional[InfluxDBClient] = None
) -> List[AvailabilityRecord]:
    client = client or get_influxdb_client()

    records = _get_points(
        client,
        "SELECT time, last(value) as available FROM available WHERE time > now() - 1h GROUP BY time(1m) FILL(previous)",
    )

    # reverse the records because they are returned in ascending order and we want descending
    #  UNFORTUNATELY InfluxDB screws up the results when you try `ORDER BY time DESC`
    records = list(reversed(records))

    if len(records) > 0:
        # Check for null-record pollution when data falls out of query scope
        if any(record.available is None for record in records):
            try:
                previous, *_ = _get_points(
                    client,
                    "SELECT time, LAST(value) as available FROM available WHERE time < now() - 1h LIMIT 1",
                )
            except:
                previous = AvailabilityRecord(False, "")

            replacement: List[AvailabilityRecord] = []

            for record in records:
                if record.available is None:
                    replacement.append(
                        AvailabilityRecord(
                            time=record.time, available=previous.available
                        )
                    )
                else:
                    replacement.append(record)

            records = replacement
    else:
        # There are no records for the previous 60 minutes, have to find the last one, and build an
        #  array for the past 60 minutes from its value
        def calc_timestamp(minutes_ago: int) -> str:
            timestamp: datetime = timezone.localtime()
            timestamp = timestamp.replace(minute=0)
            timestamp -= timedelta(minutes=minutes_ago)

            # TODO THIS TIMESTAMP STRING IS BAD
            return timestamp.isoformat("T")

        records = []

        try:
            last_seen = get_latest_availability(client)
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


def get_recent_and_latest_availability_as_serializable() -> dict:
    client: InfluxDBClient = get_influxdb_client()

    latest: dict = asdict(get_latest_availability(client))
    recent: List[dict] = list(map(asdict, get_recent_availability(client)))

    return {"latest": latest, "recent": recent}
