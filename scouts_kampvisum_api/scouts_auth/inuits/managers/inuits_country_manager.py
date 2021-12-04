from django.db import models


class InuitsCountryQuerySet(models.QuerySet):
    def sorted_by_code(self):
        return self.order_by("code")

    def sorted_by_name(self):
        return self.order_by("name")


class InuitsCountryManager(models.Manager):
    def get_queryset(self):
        return InuitsCountryQuerySet(self.model, using=self._db)

    # def get_by_natural_key(self, code):
    #     """Returns a country based on the 2-character country code."""
    #     return self.get(code=code)
    def get_by_natural_key(self, name):
        """Returns a country based on the name."""
        return self.get(name=name)
