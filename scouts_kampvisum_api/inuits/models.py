import logging
from django.db import models


logger = logging.getLogger(__name__)


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
    """

    def __init__(self, *args, **kwargs):
        kwargs['auto_now'] = False
        kwargs['auto_now_add'] = False
        kwargs['blank'] = True
        kwargs['null'] = True

        super().__init__(
            *args,
            **kwargs)

