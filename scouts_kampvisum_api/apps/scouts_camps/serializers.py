from rest_framework import serializers

from .models import ScoutsCamp


class ScoutsCampSerializer(serializers.ModelSerializer):
    """
    Serialize a ScoutsCamp object
    """
    
    class Meta:
        model = ScoutsCamp
        #fields = [ 'id', 'start_date', 'end_date', 'uuid' ]
        fields = '__all__'


class ScoutsCampDeserializer(serializers.Serializer):
    """
    Deserialize values into a ScoutsCamp object
    """
    
    name = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, data):
        return data

