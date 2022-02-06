import logging

from rest_framework import serializers

from apps.deadlines.models import Deadline, SubCategoryDeadline, CheckDeadline, DeadlineDependentDeadline
from apps.deadlines.serializers import DeadlineDateSerializer

from apps.visums.models import CampVisum
from apps.visums.serializers import CampVisumSerializer, LinkedSubCategorySerializer, LinkedCheckSerializer


logger = logging.getLogger(__name__)


class DeadlineSerializer(serializers.ModelSerializer):
    
    visum = CampVisumSerializer()
    due_date = DeadlineDateSerializer()
    
    class Meta:
        model = Deadline
        fields = "__all__"
    
    def to_internal_value(self, data: dict) -> dict:
        logger.debug("DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)
        
        visum = data.get("visum", None)
        if visum:
            visum = CampVisum.objects.safe_get(id=visum)
            if visum:
                data["visum"] = visum
        
        data = super().to_internal_value(data)
        
        logger.debug("DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)

        return data

class SubCategoryDeadlineSerializer(serializers.ModelSerializer):
    
    deadline_sub_category = LinkedSubCategorySerializer()
    
    class Meta:
        model = SubCategoryDeadline
        fields = "__all__"

class CheckDeadlineSerializer(serializers.ModelSerializer):
    
    deadline_check = LinkedCheckSerializer()
    
    class Meta:
        model = CheckDeadline
        fields = "__all__"

class DeadlineDependentDeadlineSerializer(serializers.ModelSerializer):
    
    deadline_due_after_deadline = DeadlineSerializer()
    
    class Meta:
        model = DeadlineDependentDeadline
        fields = "__all__"