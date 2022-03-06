from django.db import models


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class InuitsCountryQuerySet(models.QuerySet):
    def sorted_by_code(self):
        return self.order_by("code")

    def sorted_by_name(self):
        return self.order_by("name")


class InuitsCountryManager(models.Manager):
    def get_queryset(self):
        return InuitsCountryQuerySet(self.model, using=self._db)

    def get_by_natural_key(self, name):
        """Returns a country based on the name."""
        logger.trace(
            "GET BY NATURAL KEY %s: (name: %s (%s))",
            "InuitsCountry",
            name,
            type(name).__name__,
        )
        return self.get(name=name)
