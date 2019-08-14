from django.apps import AppConfig


class BmonitorConfig(AppConfig):
    name = "bmonitor"

    def ready(self):
        from .signals import broadcast_availability_update, AvailabilityUpdate

        AvailabilityUpdate.connect(
            broadcast_availability_update, dispatch_uid="broadcast_availability_update"
        )
