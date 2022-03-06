import datetime
from typing import List

from django.db import transaction
from django.utils import timezone

from apps.camps.models import CampYear, CampType

from apps.deadlines.models import DefaultDeadline, DeadlineDate, DeadlineItem
from apps.deadlines.services import DefaultDeadlineItemService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DefaultDeadlineService:

    default_deadline_item_service = DefaultDeadlineItemService()

    @transaction.atomic
    def get_or_create_default_deadline(
        self,
        request,
        name: str = None,
        is_important: bool = False,
        camp_year: CampYear = None,
        camp_types: List[CampType] = None,
        index: int = 0,
        label: str = "",
        description: str = "",
        explanation: str = "",
        items: list[dict] = [],
        **fields,
    ) -> DefaultDeadline:
        instance = DefaultDeadline.objects.safe_get(name=name, camp_year=camp_year)
        if instance:
            return instance

        instance = DefaultDeadline()

        instance.name = name if name else fields.get("name", None)
        instance.is_important = (
            is_important if is_important else fields.get("is_important", False)
        )
        instance.camp_year = camp_year
        instance.index = index if index else fields.get("index", 0)
        instance.label = label if label else fields.get("label", "")
        instance.description = (
            description if description else fields.get("description", "")
        )
        instance.explanation = (
            explanation if explanation else fields.get("explanation", "")
        )

        instance.full_clean()
        instance.save()

        camp_types = camp_types if camp_types else fields.get("camp_types", [])
        for camp_type in camp_types:
            instance.camp_types.add(camp_type)

        if not (
            fields
            and isinstance(fields, dict)
            and "due_date" in fields
            and isinstance(fields.get("due_date"), dict)
        ):
            fields["due_date"] = dict()
        due_date: DeadlineDate = self.get_or_create_deadline_date(
            default_deadline=instance,
            **fields.get("due_date", None),
        )

        items = items if items else fields.get("items", [])
        self.default_deadline_item_service.create_or_update_default_deadline_items(
            request=request, default_deadline=instance, items=fields.get("items", [])
        )

        return instance

    # @TODO add update
    def update_default_deadline(
        self,
        request,
        instance: DefaultDeadline,
        updated_instance: DefaultDeadline = None,
        **fields,
    ):
        instance.name = (
            updated_instance.name
            if updated_instance
            else fields.get("name", instance.name)
        )
        instance.is_important = (
            updated_instance.is_important
            if updated_instance
            else fields.get("is_important", instance.is_important)
        )
        instance.index = (
            updated_instance.index
            if updated_instance
            else fields.get("index", instance.index)
        )
        instance.label = (
            updated_instance.label
            if updated_instance
            else fields.get("label", instance.label)
        )
        instance.description = (
            updated_instance.description
            if updated_instance
            else fields.get("description", instance.description)
        )
        instance.explanation = (
            updated_instance.explanation
            if updated_instance
            else fields.get("explanation", instance.explanation)
        )

        instance.full_clean()
        instance.save()

        due_date: DeadlineDate = self.update_deadline_date(
            instance=instance.due_date, **fields.get("due_date", {})
        )

        items: List[
            DeadlineItem
        ] = self.default_deadline_item_service.create_or_update_default_deadline_items(
            request=request, default_deadline=instance, items=fields.get("items", [])
        )

        return instance

    @transaction.atomic
    def get_or_create_deadline_date(
        self, default_deadline: DefaultDeadline = None, **fields
    ) -> DeadlineDate:
        instance = DeadlineDate.objects.safe_get(default_deadline=default_deadline)
        if instance:
            return self.update_deadline_date(instance=instance, **fields)

        instance = DeadlineDate()

        instance.default_deadline = default_deadline
        instance.date_day = fields.get("date_day", None)
        instance.date_month = fields.get("date_month", None)
        instance.date_year = fields.get("date_year", None)
        instance.calculated_date = self.get_calculated_date(
            day=instance.date_day, month=instance.date_month, year=instance.date_year
        )

        instance.full_clean()
        instance.save()

        return instance

    @transaction.atomic
    def update_deadline_date(self, instance: DeadlineDate, **fields) -> DeadlineDate:
        instance.date_day = fields.get("date_day", instance.date_day)
        instance.date_month = fields.get("date_month", instance.date_month)
        instance.date_year = fields.get("date_year", instance.date_year)
        instance.calculated_date = self.get_calculated_date(
            day=instance.date_day, month=instance.date_month, year=instance.date_year
        )

        instance.full_clean()
        instance.save()

        return instance

    def get_calculated_date(
        self, day: int = None, month: int = None, year: int = None
    ) -> datetime.date:
        day = day if day else 1
        month = month if month else 1
        year = year if year else timezone.now().date().year

        return datetime.datetime(year, month, day).date()
