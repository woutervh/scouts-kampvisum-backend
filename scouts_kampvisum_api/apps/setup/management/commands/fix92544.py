import os
from pathlib import Path
from typing import List

from django.db import transaction
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from apps.deadlines.models import LinkedDeadline, LinkedDeadlineItem


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fixes issue 92544 https://redmine.inuits.eu/issues/92544"
    exception = True

    # fix for https://redmine.inuits.eu/issues/92074 for groups that were already registered
    @transaction.atomic
    def handle(self, *args, **kwargs):
        linked_deadlines: List[LinkedDeadline] = LinkedDeadline.objects.all()
        for linked_deadline in linked_deadlines:
            linked_deadline_id = linked_deadline.id
            linked_deadline_items: List[
                LinkedDeadlineItem
            ] = linked_deadline.items.all()

            for linked_deadline_item in linked_deadline_items:
                if not linked_deadline_item.linked_deadline_fix:
                    linked_deadline_item.linked_deadline_fix = linked_deadline_id

                    linked_deadline_item.full_clean()
                    linked_deadline_item.save()
