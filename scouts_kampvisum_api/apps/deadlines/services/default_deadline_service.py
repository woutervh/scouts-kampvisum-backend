import logging
import datetime

from django.db import transaction
from django.http import Http404
from django.utils import timezone

from apps.deadlines.models import DefaultDeadline, DeadlineDate, DefaultDeadlineFlag
from apps.deadlines.models.enums import DeadlineType


logger = logging.getLogger(__name__)


class DefaultDeadlineService:
    def get_or_create(
        self, name: str = None, deadline_type: DeadlineType = None, **fields
    ) -> DefaultDeadline:
        instance = DefaultDeadline.objects.safe_get(
            name=name, deadline_type=deadline_type
        )
        if instance:
            return instance

        instance = DefaultDeadline()

        instance.name = name if name else fields.get("name", None)
        instance.deadline_type = (
            deadline_type if deadline_type else fields.get("deadline_type", None)
        )
        instance.label = fields.get("label", "")
        instance.description = fields.get("description", "")
        instance.explanation = fields.get("explanation", "")
        instance.is_important = fields.get("is_important", False)

        instance.full_clean()
        instance.save()

        return instance

    def get_or_create_default_flag(
        self,
        instance: DefaultDeadlineFlag = None,
        default_deadline: DefaultDeadline = None,
        **fields
    ) -> DefaultDeadlineFlag:
        if instance and isinstance(instance, DefaultDeadlineFlag):
            instance = DefaultDeadlineFlag.objects.safe_get(id=instance.id)
            if instance:
                return instance

        name = fields.get("name", None)
        if not name:
            raise Http404("A default deadline flag requires a name, None given")

        instance = DefaultDeadlineFlag.objects.safe_get(
            default_deadline=default_deadline, name=name
        )
        if instance:
            return self.update_flag(instance=instance, **fields)

        instance = DefaultDeadlineFlag()

        instance.default_deadline = default_deadline
        instance.name = fields.get("name", "")
        instance.label = fields.get("label", instance.name)
        instance.index = fields.get("index", 0)
        instance.flag = fields.get("flag", False)

        instance.full_clean()
        instance.save()

        return instance

    def update_default_flag(
        self, instance: DefaultDeadlineFlag, **fields
    ) -> DefaultDeadlineFlag:
        instance.name = fields.get("name", instance.name)
        instance.label = fields.get("label", instance.label)
        instance.flag = fields.get("flag", instance.flag)

        instance.full_clean()
        instance.save()

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
