from typing import List

from django.db import transaction, connection
from django.db.models import Q
from django.core.management.base import BaseCommand

from scouts_auth.groupadmin.models import ScoutsUser, ScoutsFunction


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Truncate the function and group tables"
    exception = True

    @transaction.atomic
    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("truncate table scouts_auth_scoutsfunction")
            cursor.execute("truncate table scouts_auth_scoutsgroup")
