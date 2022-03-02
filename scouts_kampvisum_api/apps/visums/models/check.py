import logging

from django.db import models

from apps.visums.managers import CheckManager
from apps.visums.models import SubCategory, CheckType

from scouts_auth.inuits.models import ArchiveableAbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField, OptionalCharField
from scouts_auth.inuits.models.interfaces import (
    Explainable,
    Indexable,
    Linkable,
    Translatable,
)


logger = logging.getLogger(__name__)


class Check(
    Explainable, Indexable, Linkable, Translatable, ArchiveableAbstractBaseModel
):

    objects = CheckManager()

    name = RequiredCharField(max_length=64)
    is_multiple = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    sub_category = models.ForeignKey(
        SubCategory, related_name="checks", on_delete=models.CASCADE
    )
    check_type = models.ForeignKey(CheckType, on_delete=models.CASCADE)
    # References a method in change_notifier.py
    change_handler = OptionalCharField()

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "sub_category")

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED Check")
        return (self.name, self.sub_category)

    def has_change_handler(self):
        return True if self.change_handler else False

    def __str__(self):
        return "OBJECT Check: name({}), sub_category({}), check_type({}), is_multiple ({})".format(
            self.name, str(self.sub_category), str(self.check_type), self.is_multiple
        )
