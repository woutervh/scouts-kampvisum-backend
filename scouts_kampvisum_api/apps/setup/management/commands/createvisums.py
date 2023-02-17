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
from scouts_auth.groupadmin.models import ScoutsUser, ScoutsFunction, ScoutsToken
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

        if not count:
            count = 30

        if not access_token:
            access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ5MnZ0TVVCSG01QnVsSV9iWGs0R0lpNVQtT1NvNnJWWjBrV2FLWlJSOGZFIn0.eyJleHAiOjE2NzY2MjE0NzgsImlhdCI6MTY3NjYyMTE3OCwiYXV0aF90aW1lIjoxNjc2NjE2ODAyLCJqdGkiOiJkMTFiZjE0Yy0zY2YzLTRmMDUtYTkwZi02ZWVlZDBhMjVjYzQiLCJpc3MiOiJodHRwczovL2xvZ2luLnNjb3V0c2VuZ2lkc2VudmxhYW5kZXJlbi5iZS9hdXRoL3JlYWxtcy9zY291dHMiLCJzdWIiOiI3N2RlZDAwYy0yNjlhLTQ2OGEtODQzMS05MTg0Njc1ZGUyMmIiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJrYW1wdmlzdW0iLCJzZXNzaW9uX3N0YXRlIjoiYmI1Y2FhMTYtYWE3ZS00OTk1LTkzMTUtN2UxZmEzMTYwYjg2IiwiYWNyIjoiMCIsImFsbG93ZWQtb3JpZ2lucyI6WyIiLCJodHRwczovL2thbXAtYWNjLnNjb3V0c2VuZ2lkc2VudmxhYW5kZXJlbi5iZSIsImh0dHBzOi8va2FtcC5zY291dHNlbmdpZHNlbnZsYWFuZGVyZW4uYmUiXSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6Ikplcm9lbiBXb3V0ZXJzIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiamVyb2VuLndvdXRlcnMiLCJnaXZlbl9uYW1lIjoiSmVyb2VuIiwiZmFtaWx5X25hbWUiOiJXb3V0ZXJzIiwiZW1haWwiOiJqZXJvZW53b3V0ZXJzQGludWl0cy5ldSJ9.tUZVAR9g4JG_U12qs9nTZ4MvszUka0sLyO3KhSCdAFxWtbTf4m1P_pbwnC297MTb75kcVXNqiLpLh7EqzLut1cJXA3AHS-JEKWl97mZ913KZ4uvrwKp-3Jjuz4XtRP2a7WdxB07mvbMSeNkdWflxa-6E3iIwoTlVSIdW24HqcI2Rd2tJV3J1QhxLdlosviRtvdMOfdBpRlIRRdSxDLTg_reAMygdGoZ7kxG875zE0xRV3dUSbP1EabJ-5_Yml1coyZc57RT65kHURosXPKib7o6Yoixb3lLGwtdYIdKlx_FKCQx5jsoTjJ0YSY-TDhvqx54drDigQn3DGxGlwUlCNA'

        if not count or not access_token:
            return

        access_token = self.re_bearer.sub('', access_token)

        user: ScoutsUser = ScoutsUserSessionService.get_user_from_session(
            access_token=ScoutsToken.from_access_token(access_token))
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
