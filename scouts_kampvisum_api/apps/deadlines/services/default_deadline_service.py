import logging

from apps.deadlines.models import DefaultDeadline, DeadlineDate, DeadlineFlag
from apps.deadlines.models.enums import DeadlineType


logger = logging.getLogger(__name__)


class DefaultDeadlineService:
    def get_or_create(self, name: str, deadline_type: DeadlineType) -> DefaultDeadline:
        instance = DefaultDeadline.objects.safe_get(
            name=name, deadline_type=deadline_type
        )
        if instance:
            return instance

        instance = DefaultDeadline()

        instance.name = name
        instance.deadline_type = deadline_type

        instance.full_clean()
        instance.save()

        return instance

    def create_flag(
        self,
        default_deadline: DefaultDeadline,
        name: str,
        label: str = None,
        flag: bool = False,
    ) -> DeadlineFlag:
        instance = DeadlineFlag.objects.safe_get(
            default_deadline=default_deadline, name=name
        )
        if instance:
            return self.update_flag(
                instance=instance, **{"name": name, "label": label, "flag": flag}
            )
        instance = DeadlineFlag()

        instance.default_deadline = default_deadline
        instance.name = name
        instance.label = label if label else name

        instance.full_clean()
        instance.save()

        return instance

    def update_flag(self, instance: DeadlineFlag, **fields) -> DeadlineFlag:
        instance.name = fields.get("name", instance.name)
        instance.label = fields.get("label", instance.label)
        instance.flag = fields.get("flag", instance.flag)

        instance.full_clean()
        instance.save()

        return instance

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

        instance.full_clean()
        instance.save()

        return instance

    def update_deadline_date(self, instance: DeadlineDate, **fields) -> DeadlineDate:
        instance.date_day = fields.get("date_day", instance.date_day)
        instance.date_month = fields.get("date_month", instance.date_month)
        instance.date_year = fields.get("date_year", instance.date_year)

        instance.full_clean()
        instance.save()

        return instance
