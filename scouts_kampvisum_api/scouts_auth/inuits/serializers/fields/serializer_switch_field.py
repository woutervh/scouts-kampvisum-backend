import copy, inspect

from rest_framework import serializers
from drf_yasg2 import openapi

# Create serializer field that can switch between a create and a delete depending on id given
# Usefull for nested models in input serializers
class SerializerSwitchField(serializers.Field):
    create_serializer = None
    update_serializer = None

    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "description": (
                "Exact documentation not available, look at corresponding POST for this model to see possible fields."
                "If you want to update an existing entity make sure to also give id as field in this object"
            ),
        }

    def __init__(self, *args, **kwargs):
        self.create_serializer = kwargs.pop(
            "create_serializer", copy.deepcopy(self.create_serializer)
        )
        self.update_serializer = kwargs.pop(
            "update_serializer", copy.deepcopy(self.update_serializer)
        )
        assert (
            self.create_serializer is not None
        ), "`create_serializer` is a required argument."
        assert not inspect.isclass(
            self.create_serializer
        ), "`create_serializer` has not been instantiated."
        assert (
            self.update_serializer is not None
        ), "`update_serializer` is a required argument."
        assert not inspect.isclass(
            self.update_serializer
        ), "`update_serializer` has not been instantiated."
        super().__init__(*args, **kwargs)
        self.create_serializer.bind(field_name="", parent=self)
        self.update_serializer.bind(field_name="", parent=self)

    def to_internal_value(self, data):
        if data.get("id", None):
            return self.update_serializer.run_validation(data)
        else:
            return self.create_serializer.run_validation(data)
