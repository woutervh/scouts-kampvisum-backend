import logging

from rest_framework import serializers

from apps.people.models import InuitsParticipant
from apps.people.serializers import InuitsMemberSerializer, InuitsNonMemberSerializer


logger = logging.getLogger(__name__)


class InuitsParticipantSerializer(serializers.ModelSerializer):
    
    member = InuitsMemberSerializer()
    non_member = InuitsNonMemberSerializer()
    
    class Meta:
        model = InuitsParticipant
        fields = "__all__"
