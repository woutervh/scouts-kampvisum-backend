import django_filters
from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP
from scouts_auth.inuits.filters import BaseQueryArrayField


class MultipleUUIDFilter(django_filters.BaseCSVFilter, django_filters.UUIDFilter):
    """
    Filter that accepts multiple ids and does an or query for every uuid.
    Uses QueryArrayWidget in the background so url syntax is for example:

    ?theme[]=1de4a9bb-673e-4ae9-8653-4b7a708e91d3&theme[]=594862ca-f1cd-4bf1-b408-0fbaa210ba54
    OR
    theme=1de4a9bb-673e-4ae9-8653-4b7a708e91d3&theme=594862ca-f1cd-4bf1-b408-0fbaa210ba54
    """

    base_field_class = BaseQueryArrayField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "help_text", ("A list of uuids given as query array (with or without []).")
        )
        kwargs.setdefault("lookup_expr", "exact")
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        # value is either a list or an 'empty' value
        values = value or []
        # Combine uuid filter calls with OR
        q = Q()
        for value in values:
            if value in django_filters.constants.EMPTY_VALUES:
                break
            lookup = LOOKUP_SEP.join([self.field_name, self.lookup_expr])
            q |= Q(**{lookup: value})

        qs = qs.filter(q)
        return qs
