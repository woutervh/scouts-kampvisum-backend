from rest_framework import serializers

from ..models import CampYear
from inuits.serializers.fields import OptionalDateField, RequiredYearField


class CampYearSerializer(serializers.ModelSerializer):

    year = RequiredYearField()
    start_date = OptionalDateField()
    end_date = OptionalDateField()

    class Meta:
        model = CampYear
        fields = '__all__'
