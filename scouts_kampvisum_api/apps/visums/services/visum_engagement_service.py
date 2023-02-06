from django.db import transaction
from django.core.exceptions import ValidationError

from apps.visums.models import CampVisum, CampVisumEngagement

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
    def update_engagement(
        self, request, instance: CampVisumEngagement, **fields
    ) -> CampVisumEngagement:
        user: ScoutsUser = request.user
        visum: CampVisum = instance.visum

        if user.has_role_district_commissioner(group_admin_id=visum.group):
            if instance.leaders and instance.group_leaders:
                instance.district_commissioner = user
                instance.approved = True
            elif not instance.leaders:
                instance.leaders = user
            else:
                instance.group_leaders = user

        elif user.has_role_group_leader(group_admin_id=visum.group):
            if not instance.leaders:
                instance.leaders = user
            else:
                instance.group_leaders = user
        elif user.has_role_leader(group_admin_id=visum.group):
            instance.leaders = user
        else:
            raise ValidationError(
                "Only leaders, group leaders and DC's can sign a camp"
            )

        instance.full_clean()
        instance.save()

        return instance

    def is_signable_by_dc(self, request, instance: CampVisumEngagement) -> bool:
        visum: CampVisum = instance.visum

        return visum.is_signable()
