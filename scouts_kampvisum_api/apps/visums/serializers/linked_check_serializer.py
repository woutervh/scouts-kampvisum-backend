from rest_framework import serializers

from apps.visums.models import LinkedCheck
from apps.visums.serializers import VisumCheckSerializer
from apps.visums.urls import LinkedCheckEndpointFactory


class LinkedCheckSerializer(serializers.ModelSerializer):

    parent = VisumCheckSerializer()
    endpoint = serializers.SerializerMethodField()

    class Meta:
        model = LinkedCheck
        exclude = ["sub_category"]

    def get_endpoint(self, obj: LinkedCheck):
        return LinkedCheckEndpointFactory.get_endpoint(
            "{}/{}/".format(obj.parent.check_type.endpoint_route, obj.id)
        )
