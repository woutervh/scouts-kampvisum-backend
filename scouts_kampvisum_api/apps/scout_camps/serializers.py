'''
Created on Jul 27, 2021

@author: boro
'''
from rest_framework import serializers
from .models import Camp


class CampOutputSerializer(serializers.ModelSerializer):
    '''
    Serialize a Camp object
    '''
    
    class Meta:
        model = Camp
        #fields = [ 'id', 'start_date', 'end_date', 'uuid' ]
        fields = '__all__'

class CampInputSerializer(serializers.Serializer):
    '''
    Deserialize values into a Camp object
    '''
    
    name = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, data):
        return data

