'''
Created on Jul 27, 2021

@author: boro
'''
from rest_framework import serializers
from .models import ScoutsTroopName


class ScoutsTroopNameSerializer(serializers.ModelSerializer):
    '''
    Serialize a ScoutTroopName object
    '''
    
    class Meta:
        model = ScoutsTroopName
        #fields = [ 'id', 'start_date', 'end_date', 'uuid' ]
        fields = '__all__'

class ScoutsTroopNameDeserializer(serializers.Serializer):
    '''
    Deserialize values into a Camp object
    '''
    
    name = serializers.CharField()

    def validate(self, data):
        return data

