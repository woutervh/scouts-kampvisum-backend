from django.db import transaction
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.visums.models import CampVisum
from apps.visums.models.enums import CampVisumState


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fixes visum.status from DATA_REQUIRED to SIGNABLE if all deadline checks are filled"
    exception = True

    @transaction.atomic
    def handle(self, *args, **kwargs):
        visums = CampVisum.objects.all()
        for visum in visums:
            if visum.state == CampVisumState.DATA_REQUIRED:
                from apps.deadlines.services import LinkedDeadlineService
                if LinkedDeadlineService().are_camp_registration_deadline_items_checked(
                    visum=visum
                ):
                    visum.state = CampVisumState.SIGNABLE
                    logger.debug(f"State of CampVisum {visum.name} was changed to SIGNABLE")
                    visum.updated_on = timezone.now()
                    visum.full_clean()
                    visum.save()