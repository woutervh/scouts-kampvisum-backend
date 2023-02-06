from django.db import models
from django.core.exceptions import ValidationError

from scouts_auth.groupadmin.models import ScoutsUser

from scouts_auth.inuits.models import AbstractBaseModel


class CampVisumEngagementQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CampVisumEngagementManager(models.Manager):
    def get_queryset(self):
        return CampVisumEngagementQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except Exception:
                pass

        if raise_error:
            raise ValidationError(
                f"Unable to locate CampVisumEngagement instance(s) with the provided params: (id: {pk})"
            )

        return None


class CampVisumEngagement(AbstractBaseModel):

    objects = CampVisumEngagementManager()

    approved = models.BooleanField(default=False)

    leaders = models.ForeignKey(
        ScoutsUser,
        on_delete=models.DO_NOTHING,
        related_name="%(class)s_leaders",
        null=True,
        blank=True,
    )
    group_leaders = models.ForeignKey(
        ScoutsUser,
        on_delete=models.DO_NOTHING,
        related_name="%(class)s_group_leaders",
        null=True,
        blank=True,
    )
    district_commissioner = models.ForeignKey(
        ScoutsUser,
        on_delete=models.DO_NOTHING,
        related_name="%(class)s_district_commissioner",
        null=True,
        blank=True,
    )

    def can_sign(self) -> bool:
        return self.approved

    def leaders_can_sign(self) -> bool:
        return self.can_sign()

    def group_leaders_can_sign(self) -> bool:
        return self.leaders_can_sign() and self.leaders is not None

    def district_commissioner_can_sign(self) -> bool:
        return self.group_leaders_can_sign() and self.group_leaders is not None

    def __str__(self):
        return f"CampVisumEngagement ({self.id}): leaders ({self.leaders.username if self.leaders else None}), group_leaders ({self.group_leaders.username if self.group_leaders else None}), district_commissioner ({self.district_commissioner.username if self.district_commissioner else None})"
