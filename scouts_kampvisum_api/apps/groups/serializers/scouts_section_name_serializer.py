import logging
from rest_framework import serializers

from apps.groups.models import ScoutsSectionName

from scouts_auth.groupadmin.scouts import AgeGroup
from scouts_auth.inuits.models import Gender


logger = logging.getLogger(__name__)


class ScoutsSectionNameSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutSectionName object
    """

    name = serializers.CharField(max_length=128)
    gender = serializers.ChoiceField(choices=Gender, default=Gender.MIXED)
    age_group = serializers.ChoiceField(
        choices=AgeGroup, default=AgeGroup.AGE_GROUP_UNKNOWN
    )

    class Meta:
        model = ScoutsSectionName
        fields = "__all__"


class ScoutsSectionNameAPISerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsSectionName object for API transactions.
    """

    class Meta:
        model = ScoutsSectionName
        fields = ["name"]
