from rest_framework import serializers

from ..models import CampVisumSubCategory
#from ..serializers import CampVisumCategorySerializer


class CampVisumSubCategorySerializer(serializers.ModelSerializer):

    #category = CampVisumCategorySerializer()
    name = serializers.CharField(max_length=128)

    class Meta:
        model = CampVisumSubCategory()
        fields = '__all__'

#    def create(self, validated_data) -> CampVisumSubCategory:
#        """Deserializes a stream into a CampVisumSubCategory object."""
#        return CampVisumSubCategory(**validated_data)
#
#    def update(self, instance, validated_data):
#        """Serializes a CampVisumSubCategory object into a stream."""
#        instance.category =


class CampVisumSubCategoryAPISerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    class Meta:
        model = CampVisumSubCategory()
        fields = ['name', 'uuid', 'status']

    def get_status(self, obj):
        return False
