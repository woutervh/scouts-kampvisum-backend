import logging
import datetime
from dateutil.relativedelta import relativedelta

from django.db import models
from django.db.models.functions import Concat
from django.db.models import Q
from django_filters import FilterSet, CharFilter, NumberFilter

from apps.participants.models import InuitsParticipant

from scouts_auth.inuits.models import GenderHelper


logger = logging.getLogger(__name__)


class InuitsParticipantFilter(FilterSet):
    term = CharFilter(method="search_term_filter")
    min_age = NumberFilter(method="search_min_age_filter")
    max_age = NumberFilter(method="search_max_age_filter")
    gender = CharFilter(method="search_gender_filter")

    class Meta:
        model = InuitsParticipant
        fields = []

    def search_term_filter(self, queryset, name, value):
        # Annotate full name so we can do an icontains on the entire name
        return (
            queryset.annotate(
                full_name_1=Concat(
                    "first_name", "last_name", output_field=models.CharField()
                )
            )
            .annotate(
                full_name_2=Concat(
                    "last_name", "first_name", output_field=models.CharField()
                )
            )
            .filter(Q(full_name_1__icontains=value) | Q(full_name_2__icontains=value))
        )

    def search_min_age_filter(self, queryset, name, value):
        logger.debug(
            "MIN DATE: %s", datetime.datetime.now() - relativedelta(years=value)
        )
        return queryset.filter(
            birth_date__lt=datetime.datetime.now() - relativedelta(years=value)
        )

    def search_max_age_filter(self, queryset, name, value):
        logger.debug(
            "MAX DATE: %s", datetime.datetime.now() - relativedelta(years=value)
        )
        return queryset.filter(
            birth_date__gt=datetime.datetime.now() - relativedelta(years=value)
        )

    def search_gender_filter(self, queryset, name, value):
        return queryset.filter(gender=GenderHelper.parse_gender(value))
