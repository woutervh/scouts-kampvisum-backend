from typing import List

from django.db import transaction
from django.db.models import Q
from django.core.management.base import BaseCommand

from scouts_auth.groupadmin.models import ScoutsUser, ScoutsFunction


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fixes issue 91782 https://redmine.inuits.eu/issues/91782"
    exception = True

    # fix for https://redmine.inuits.eu/issues/91782 for functions that had too many groups
    @transaction.atomic
    def handle(self, *args, **kwargs):
        users: List[ScoutsUser] = ScoutsUser.objects.all()

        for user in users:
            user._persisted_scouts_groups.clear()
            user._persisted_scouts_functions.clear()

        logger.debug(
            "Removed persisted groups and functions for %d users", len(users))

        functions: List[ScoutsFunction] = ScoutsFunction.objects.all()
        for function in functions:
            function.delete()

        logger.debug("Removed %d ScoutsFunction instance(s)", len(functions))
