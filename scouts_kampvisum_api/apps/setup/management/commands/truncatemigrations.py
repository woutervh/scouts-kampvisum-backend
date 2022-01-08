import logging

from django.db import connection
from django.core.management.base import BaseCommand


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Truncates django's migrations table"
    exception = False

    def handle(self, *args, **kwargs):
        from apps.camps.services import CampYearService

        logger.debug("Truncating migrations table")

        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE django_migrations")
