import logging

from django.apps import AppConfig


logger = logging.getLogger(__name__)


class ScoutsAuthConfig(AppConfig):
    name = "scouts_auth"

    def ready(self):
        from scouts_auth.auth.signals import ScoutsAuthSignalSender

        ScoutsAuthSignalSender().send_app_ready()
