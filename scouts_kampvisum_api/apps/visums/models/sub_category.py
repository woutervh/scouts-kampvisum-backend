from django.db import models

from apps.camps.models import CampType

from apps.visums.models import Category
from apps.visums.managers import SubCategoryManager

from scouts_auth.inuits.models import ArchiveableAbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField
from scouts_auth.inuits.models.interfaces import (
    Describable,
    Explainable,
    Indexable,
    Linkable,
    Translatable,
)

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class SubCategory(
    Describable,
    Explainable,
    Indexable,
    Linkable,
    Translatable,
    ArchiveableAbstractBaseModel,
):

    objects = SubCategoryManager()

    category = models.ForeignKey(
        Category,
        related_name="sub_categories",
        on_delete=models.CASCADE,
    )
    name = RequiredCharField(max_length=128)
    camp_types = models.ManyToManyField(CampType)

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "category")

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED SubCategory")
        return (self.name, self.category)

    def __str__(self):
        return "OBJECT SubCategory: name({}), label ({}), index ({}), explanation ({}), description ({}), link ({}), category({})".format(
            self.name,
            self.label,
            self.index,
            self.explanation,
            self.description,
            self.link,
            self.category,
        )

    def to_simple_str(self):
        return "{} ({})".format(self.id, self.name)
