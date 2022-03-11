from django.db import models
from django.core.exceptions import ValidationError


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineItemQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DeadlineItemManager(models.Manager):
    def get_queryset(self):
        return DeadlineItemQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        deadline = kwargs.get("deadline", None)
        item_flag = kwargs.get("item_flag", None)
        item_sub_category = kwargs.get("item_sub_category", None)
        item_check = kwargs.get("item_check", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if deadline:
            if item_flag:
                from apps.deadlines.models import DeadlineFlag

                if isinstance(item_flag, DeadlineFlag):
                    item_flag = item_flag.id
                else:
                    flag = DeadlineFlag.objects.safe_get(**item_flag)
                    if flag:
                        item_flag = flag.id

                try:
                    return self.get_queryset().get(
                        deadline=deadline, item_flag__id=item_flag
                    )
                except:
                    pass

            if item_sub_category:
                from apps.visums.models import SubCategory

                if isinstance(item_sub_category, SubCategory):
                    item_sub_category = item_sub_category.id
                else:
                    sub_category = SubCategory.objects.get_by_natural_key(
                        item_sub_category[0], item_sub_category[1]
                    )
                    if sub_category:
                        item_sub_category = sub_category.id

                try:
                    return self.get_queryset().get(
                        deadline=deadline, item_sub_category__id=item_sub_category
                    )
                except:
                    pass

            if item_check:
                from apps.visums.models import Check

                if isinstance(item_check, Check):
                    item_check = item_check.id
                else:
                    check = Check.objects.get_by_natural_key(
                        item_check[0], item_check[1]
                    )
                    if check:
                        item_check = check.id

                try:
                    return self.get_queryset().get(
                        deadline=deadline, item_check__id=item_check
                    )
                except:
                    pass

        if raise_error:
            raise ValidationError(
                "Unable to locate DeadlineItem instance(s) with the provided params: (id: {}, (deadline: {}, (item_flag: {}, item_sub_category: {}, item_check: {}))".format(
                    pk,
                    deadline,
                    item_flag,
                    item_sub_category,
                    item_check,
                )
            )
        return None
