from django.db import transaction

from apps.visums.models import CampVisumEngagement

from scouts_auth.groupadmin.models import ScoutsUser


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumEngagementService:
    @transaction.atomic
    def create_engagement(self, *args, **kwargs):
        approval = CampVisumEngagement()

        approval.full_clean()
        approval.save()

        return approval

    @transaction.atomic
    def update_engagement(self, request, instance: CampVisumEngagement, **fields):
        instance.approved = fields.get("approved", False)
        instance.leaders = fields.get("leaders", None)
        instance.group_leaders = fields.get("group_leaders", None)
        instance.district_commissioner = fields.get("district_commissioner", None)

        instance.full_clean()
        instance.save()

        return instance
