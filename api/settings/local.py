from .common import *  # noqa

DEBUG = True

# Channels

ASGI_APPLICATION = "api.routing.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    }
}

ROOM_GROUP_NAME = "Alexandria"

# InfluxDB

INFLUXDB_HOST = "localhost"
INFLUXDB_PORT = 8086
INFLUXDB_USERNAME = None
INFLUXDB_PASSWORD = None
INFLUXDB_DATABASE = "bathroom"
INFLUXDB_TIMEOUT = 10

API_PASSWORD = "42"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "n3ya)e3j#4&^!h67w-u2oc)w#a$r9+2fqy+!#*oquwo^ow0lo#"
