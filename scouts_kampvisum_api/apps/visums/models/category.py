import logging

from django.db import models

from apps.camps.models import CampYear

from apps.visums.managers import CategoryManager
from apps.visums.models import CampType

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.interfaces import (
    Describable,
    Explainable,
    Indexable,
    Translatable,
)
from scouts_auth.inuits.models.fields import RequiredCharField


logger = logging.getLogger(__name__)


class Category(Describable, Explainable, Indexable, Translatable, AbstractBaseModel):

    objects = CategoryManager()

    name = RequiredCharField(max_length=128)
    camp_year = models.ForeignKey(
        CampYear, on_delete=models.CASCADE, related_name="categories"
    )
    camp_types = models.ManyToManyField(CampType)

    class Meta:
        ordering = ["index"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "camp_year"], name="unique_category_name_and_camp_year"
            )
        ]

    def natural_key(self):
        logger.debug("NATURAL KEY CALLED Category")
        return (self.name, self.camp_year)

    def __str__(self):
        return "OBJECT Category: name({}), camp_year ({}), label({}), index({}), description({}), explanation ({})".format(
            self.name,
            self.camp_year,
            self.label,
            self.index,
            self.description,
            self.explanation,
        )
