from rest_framework import serializers

from .models import ScoutsCampVisumSubCategory
from ..categories.serializers import ScoutsCampVisumCategorySerializer


class ScoutsCampVisumSubCategorySerializer(serializers.ModelSerializer):
    
    category = ScoutsCampVisumCategorySerializer()
    name = serializers.CharField(max_length=128)
    
    class Meta:
        model = ScoutsCampVisumSubCategory()
        fields = '__all__'
    
#    def create(self, validated_data) -> ScoutsCampVisumSubCategory:
#        """Deserializes a stream into a ScoutsCampVisumSubCategory object."""
#        return ScoutsCampVisumSubCategory(**validated_data)
#    
#    def update(self, instance, validated_data):
#        """Serializes a ScoutsCampVisumSubCategory object into a stream."""
#        instance.category = 

