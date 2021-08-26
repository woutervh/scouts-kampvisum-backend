from rest_framework import serializers

from ..models import CampVisumCategory
from inuits.serializers.fields import OptionalCharField, RequiredIntegerField


class CampVisumCategorySerializer(serializers.ModelSerializer):
    
    name = serializers.CharField(max_length=128)
    index = RequiredIntegerField()
    description = OptionalCharField()
    
    class Meta:
        model = CampVisumCategory()
        fields = '__all__'
    
#    def create(self, validated_data) -> CampVisumCategory:
#        """Deserializes a stream into a CampVisumCategory object."""
#        return CampVisumCategory(**validated_data)
#   
#    def update(self, instance, validated_data):
#        """Serializes a CampVisumCategory object into a stream."""
#        instance.name = validated_data.get('name', instance.name)
#        
#        return instance

