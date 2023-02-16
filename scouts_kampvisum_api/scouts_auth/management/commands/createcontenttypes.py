from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Sets up content types for scouts_auth"
    exception = False

    def handle(self, *args, **kwargs):
        app_label = "scouts_auth"
        model = "PersistedFile".lower()

        ct = self.get_contenttype(app_label, model)

        if not ct:
            logger.error(
                f"Couldn't create content type for model {model} in app {app_label}")

            return

        default_permissions = ["add", "change", "view", "delete"]
        for default_permission in default_permissions:
            perm = self.get_permission(
                name=f"User can {default_permission} a persisted file",
                content_type=ct,
                codename=f"{default_permission}_{model}")

    def get_contenttype(self, app_label: str, model: str):
        try:
            ct = ContentType.objects.get(
                app_label=app_label, model=model)
        except Exception:
            ct = None

        if not ct:
            ct = ContentType()

            ct.app_label = app_label
            ct.model = model

            ct.full_clean()
            ct.save()

        return ct

    def get_permission(self, name, content_type, codename):
        try:
            permission = Permission.objects.get(
                name=name, content_type=content_type, codename=codename)
        except Exception:
            permission = None

        if not permission:
            permission = Permission()

            permission.name = name
            permission.content_type = content_type
            permission.codename = codename

            permission.full_clean()
            permission.save()

        return permission
