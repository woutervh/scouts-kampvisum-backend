import logging
from rest_framework import serializers

from ..models import SectionName
from apps.groupadmin.api import MemberGender, AgeGroup


logger = logging.getLogger(__name__)


class SectionNameSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutSectionName object
    """

    name = serializers.CharField(max_length=128)
    gender = serializers.ChoiceField(choices=MemberGender, default=MemberGender.MIXED)
    age_group = serializers.ChoiceField(
        choices=AgeGroup, default=AgeGroup.AGE_GROUP_UNKNOWN
    )

    class Meta:
        model = SectionName
        fields = "__all__"


class SectionNameAPISerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutsSectionName object for API transactions.
    """

    class Meta:
        model = SectionName
        fields = ["name"]
