from rest_framework import serializers

from ..models import SubCategory
from ..serializers import CategorySerializer


class SubCategorySerializer(serializers.ModelSerializer):
    
    category = CategorySerializer()
    name = serializers.CharField(max_length=128)
    
    class Meta:
        model = SubCategory()
        fields = '__all__'
    
#    def create(self, validated_data) -> SubCategory:
#        """Deserializes a stream into a SubCategory object."""
#        return SubCategory(**validated_data)
#    
#    def update(self, instance, validated_data):
#        """Serializes a SubCategory object into a stream."""
#        instance.category = 

