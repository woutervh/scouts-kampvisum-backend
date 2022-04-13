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

    # fix for https://redmine.inuits.eu/issues/92074 to reestablish the link between LinkedDeadline and LinkedDeadlineItem
    @transaction.atomic
    def handle(self, *args, **kwargs):
        linked_deadline_items: List[
            LinkedDeadlineItem
        ] = LinkedDeadlineItem.objects.all()
        for linked_deadline_item in linked_deadline_items:
            if linked_deadline_item.linked_deadline_fix:
                linked_deadline: LinkedDeadline = LinkedDeadline.objects.safe_get(
                    id=linked_deadline_item.linked_deadline_fix
                )
                if linked_deadline:
                    linked_deadline_item.linked_deadline = linked_deadline

                    linked_deadline_item.full_clean()
                    linked_deadline_item.save()

        linked_deadline_items: List[LinkedDeadlineItem] = list(
            LinkedDeadlineItem.objects.all().filter(
                Q(linked_deadline_fix__isnull=True) | Q(linked_deadline_fix__exact="")
            )
        )
        logger.info(
            "LinkedDeadlineItem instances not linked to a LinkedDeadline: %d",
            len(linked_deadline_items),
        )

        # Double check
        visums: List[CampVisum] = CampVisum.objects.all()
        for visum in visums:
            deadlines: List[LinkedDeadline] = visum.deadlines.all()
            for deadline in deadlines:
                items: List[LinkedDeadlineItem] = deadline.items.all()
                for item in items:
                    if not item.linked_deadline_fix:
                        raise ValidationError(
                            "LinkedDeadlineItem %s (%s) does not have a linked_deadline_fix !"
                        )
        logger.info("All linked deadline items have the fix !")
