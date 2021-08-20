from rest_framework import serializers

class OptionalDateField(serializers.DateField):

    def __init__(self, *args, **kwargs):
        kwargs['required'] = False
        super(OptionalDateField, self).__init__(*args, **kwargs)

