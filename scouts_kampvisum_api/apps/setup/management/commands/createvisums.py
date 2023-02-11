from typing import List

from django.db import transaction
from django.db.models import Q
from django.core.management.base import BaseCommand

from apps.groups.models import ScoutsSection
from apps.visums.models import CampVisum
from apps.visums.services import CampVisumService

from scouts_auth.auth.exceptions import ScoutsAuthException
from scouts_auth.groupadmin.models import ScoutsUser, ScoutsFunction
from scouts_auth.scouts.services import ScoutsUserSessionService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fixes issue 91782 https://redmine.inuits.eu/issues/91782"
    exception = True

    visum_service = CampVisumService()
    
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('poll_id', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete poll instead of closing it',
        )

    # fix for https://redmine.inuits.eu/issues/91782 for functions that had too many groups
    @transaction.atomic
    def handle(self, count: int = 10, access_token: str = None, *args, **kwargs):

        logger.debug(f"CREATING {count} visums per group")
        logger.debug(f"ACCESS_TOKEN: {access_token}")

        user: ScoutsUser = ScoutsUserSessionService.get_user_from_session(access_token=access_token)
        if not user:
            raise ScoutsAuthException("Unable to find user with provided access token")
        
        for scouts_group in user.get_scouts_groups():
            section: ScoutsSection = ScoutsSection.objects.all().first()

            for x in range(count):
                data: dict = {
                    "group": scouts_group.group_admin_id,
                    "group_name": scouts_group.name,
                    "year": 2023,
                    "name": f"INUITS speed test {scouts_group.group_admin_id} {counter:03}",
                    "start_date": "",
                    "end_date": "",
                    "sections": [section.id],
                    "camp_types": [],
                }

                visum: CampVisum = self.visum_service.visum_create(**data)

                logger.debug(f"Created visum {visum.name} for group {visum.group}")


