from typing import List

from django.db import transaction
from django.db.models import Q
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from apps.deadlines.models import LinkedDeadline, LinkedDeadlineItem

from apps.visums.models import CampVisum


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fixes issue 92544 https://redmine.inuits.eu/issues/92544"
    exception = True

    # fix for https://redmine.inuits.eu/issues/92074 to remove the previous fixes
    @transaction.atomic
    def handle(self, *args, **kwargs):
        linked_deadline_items: List[LinkedDeadlineItem] = list(
            LinkedDeadlineItem.objects.all().filter(Q(linked_deadline__isnull=True))
        )
        logger.info(
            "LinkedDeadlineItem instances not linked to a LinkedDeadline: %d",
            len(linked_deadline_items),
        )

        for linked_deadline_item in linked_deadline_items:
            linked_deadline_item.delete()
