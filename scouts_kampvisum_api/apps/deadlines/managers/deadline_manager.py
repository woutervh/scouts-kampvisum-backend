from django.db import models
from django.core.exceptions import ValidationError


import logging

logger = logging.getLogger(__name__)


class DeadlineQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DeadlineManager(models.Manager):
    def get_queryset(self):
        return DeadlineQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        parent = kwargs.get("parent", None)
        visum = kwargs.get("visum", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if parent and visum:
            try:
                return self.get_queryset().get(parent=parent, visum=visum)
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate Deadline instance with provided params (pk: {}, (parent: {}, visum: {}))".format(
                    pk, parent, visum
                )
            )
        return None


class LinkedSubCategoryDeadlineQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinkedSubCategoryDeadlineManager(models.Manager):
    def get_queryset(self):
        return LinkedSubCategoryDeadlineQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        parent = kwargs.get("parent", None)
        visum = kwargs.get("visum", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if parent and visum:
            try:
                return self.get_queryset().get(parent=parent, visum=visum)
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate LinkedSubCategoryDeadline instance with provided params (pk: {}, (parent: {}, visum: {}))".format(
                    pk, parent, visum
                )
            )

        return None


class LinkedCheckDeadlineQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinkedCheckDeadlineManager(models.Manager):
    def get_queryset(self):
        return LinkedCheckDeadlineQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        parent = kwargs.get("parent", None)
        visum = kwargs.get("visum", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if parent and visum:
            try:
                return self.get_queryset().get(parent=parent, visum=visum)
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate LinkedCheckDeadline instance with provided params (pk: {}, (parent: {}, visum: {}))".format(
                    pk, parent, visum
                )
            )

        return None


class MixedDeadlineQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MixedDeadlineManager(models.Manager):
    def get_queryset(self):
        return MixedDeadlineQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        parent = kwargs.get("parent", None)
        visum = kwargs.get("visum", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if parent and visum:
            try:
                return self.get_queryset().get(parent=parent, visum=visum)
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate MixedDeadline instance with provided params (pk: {}, (parent: {}, visum: {}))".format(
                    pk, parent, visum
                )
            )

        return None
