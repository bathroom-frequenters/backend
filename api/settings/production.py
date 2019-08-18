from .common import *  # noqa

# Channels

ASGI_APPLICATION = "api.routing.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("redis", 6379)]},
    }
}

ROOM_GROUP_NAME = "Alexandria"

# InfluxDB

INFLUXDB_HOST = "db"
INFLUXDB_PORT = 8086
INFLUXDB_USERNAME = None
INFLUXDB_PASSWORD = None
INFLUXDB_DATABASE = "bathroom"
INFLUXDB_TIMEOUT = 10

# CHANGE ME!
API_PASSWORD = "42"
