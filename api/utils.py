from django.conf import settings
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError


# thanks to https://stackoverflow.com/a/52580214
def get_influxdb_client() -> InfluxDBClient:
    client = InfluxDBClient(
        settings.INFLUXDB_HOST,
        settings.INFLUXDB_PORT,
        settings.INFLUXDB_USERNAME,
        settings.INFLUXDB_PASSWORD,
        settings.INFLUXDB_DATABASE,
        timeout=getattr(settings, "INFLUXDB_TIMEOUT", 10),
        ssl=getattr(settings, "INFLUXDB_SSL", False),
        verify_ssl=getattr(settings, "INFLUXDB_VERIFY_SSL", False),
    )

    # Create database if it does not exist
    try:
        client.create_database(settings.INFLUXDB_DATABASE)
    except InfluxDBClientError:
        pass

    return client
