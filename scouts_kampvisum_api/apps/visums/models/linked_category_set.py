from django.db import models

from apps.visums.models import CampVisum
from apps.visums.models.enums import CheckState

from scouts_auth.inuits.models import AbstractBaseModel


class LinkedCategorySetQuerySet(models.QuerySet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinkedCategorySetManager(models.Manager):
    def get_queryset(self):
        return LinkedCategorySetQuerySet(self.model, using=self._db).prefetch_related('categories')

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        visum = kwargs.get("visum", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if visum:
            try:
                return self.get_queryset().get(visum=visum)
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate CampVisum instance(s) with the provided params: (id: {})".format(
                    pk,
                )
            )

        return None


class LinkedCategorySet(AbstractBaseModel):

    objects = LinkedCategorySetManager()

    visum = models.OneToOneField(
        CampVisum, on_delete=models.CASCADE, related_name="category_set"
    )

    class Meta:
        indexes = [
            models.Index(fields=['visum'], name='visum_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['visum'], name='unique_visum_for_set')
        ]

    def is_checked(self) -> CheckState:
        categories = self.categories.all()
        for category in categories:
            if not category.is_checked():
                return CheckState.UNCHECKED
        return CheckState.CHECKED

    @property
    def readable_name(self):
        return "{} {}".format(
            self.visum.year.year,
            ",".join(
                camp_type.camp_type for camp_type in self.visum.camp_types.all()),
        )
