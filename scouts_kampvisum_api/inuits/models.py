import logging, warnings
from django.db import models


logger = logging.getLogger(__name__)


class OptionalCharField(models.CharField):
    """
    Initializes a models.CharField as optional.

    This is equivalent to setting a models.CharField as such:
    some_optional_char_field = models.CharField(
        blank=True,
    )
    If a default value is passed, it is discarded.

    @see https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.Field.null
    """
    def __init__(self, *args, **kwargs):
        if 'default' in kwargs:
            kwargs.pop('default', None)
            warnings.warn("A default value was passed and was discarded\
                Use models.CharField if this field needs a default.")
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)


class OptionalIntegerField(models.IntegerField):
    """
    Initializes a models.IntegerField as optional.

    This is equivalent to setting a models.IntegerField as such:
    some_optional_integer_field = models.IntegerField(
        blank=True,
        null=True,
    )
    If a default value is passed, it is discarded.
    """
    def __init__(self, *args, **kwargs):
        if 'default' in kwargs:
            kwargs.pop('default', None)
            warnings.warn("A default value was passed and was discarded\
                Use models.IntegerField if this field needs a default.")
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(*args, **kwargs)


class OptionalDateField(models.DateField):
    """
    Initializes a models.DateField as optional.

    This is equivalent to setting a models.DateField as such:
    some_optional_date_field = models.DateField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )
    If a default value is passed, it is discarded.
    """
    def __init__(self, *args, **kwargs):
        if 'default' in kwargs:
            kwargs.pop('default', None)
            warnings.warn("A default value was passed and was discarded\
                Use models.DateField if this field needs a default.")
        kwargs['auto_now'] = False
        kwargs['auto_now_add'] = False
        kwargs['blank'] = True
        kwargs['null'] = True

        super().__init__(*args, **kwargs)

