from rest_framework import serializers

from ..models import ScoutsCampVisumCategory


class ScoutsCampVisumCategorySerializer(serializers.ModelSerializer):
    
    name = serializers.CharField(max_length=128)
    
    class Meta:
        model = ScoutsCampVisumCategory()
        fields = '__all__'
    
#    def create(self, validated_data) -> ScoutsCampVisumCategory:
#        """Deserializes a stream into a ScoutsCampVisumCategory object."""
#        return ScoutsCampVisumCategory(**validated_data)
#   
#    def update(self, instance, validated_data):
#        """Serializes a ScoutsCampVisumCategory object into a stream."""
#        instance.name = validated_data.get('name', instance.name)
#        
#        return instance

