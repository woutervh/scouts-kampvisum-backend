import re
from types import SimpleNamespace
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
    help = "Creates the specified amount of test visums for each of the user's scouts groups"
    exception = True

    visum_service = CampVisumService()

    default_count = 10
    default_start = 0
    re_bearer = re.compile(re.escape('bearer'), re.IGNORECASE)

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--count',
            type=int,
            dest='count',
            default=self.default_count,
            help='Number of visums to create for each group',
        )
        parser.add_argument(
            '-s',
            '--start',
            type=int,
            dest='start',
            default=self.default_start,
            help='Index to start counting from',
        )
        parser.add_argument(
            '-t',
            '--token',
            type=str,
            dest='access_token',
            default='',
            help='Valid and active access token to retrieve a scouts user',
        )

    # fix for https://redmine.inuits.eu/issues/91782 for functions that had too many groups
    @transaction.atomic
    def handle(self, *args, **options):
        count: int = options.get('count', self.default_count)
        start: int = options.get('start', self.default_start)
        access_token: str = options.get('access_token', None)

        if not count or not access_token:
            return

        access_token = self.re_bearer.sub('', access_token)

        user: ScoutsUser = ScoutsUserSessionService.get_user_from_session(
            access_token=access_token)
        if not user:
            raise ScoutsAuthException(
                "Unable to find user with provided access token")

        group_count = -1
        for scouts_group in user.get_scouts_groups():
            group_count += 1

            if group_count == 0:
                continue

            section: ScoutsSection = ScoutsSection.objects.all().first()

            for x in range(start, start + count):
                data: dict = {
                    "group": scouts_group.group_admin_id,
                    "group_name": scouts_group.name,
                    "name": f"INUITS speed test {scouts_group.group_admin_id} {x:03}",
                    "sections": [section.id],
                }

                visum: CampVisum = self.visum_service.visum_create(
                    request=SimpleNamespace(user=user), **data)

                logger.debug(
                    f"Created visum {visum.name} for group {visum.group}")
