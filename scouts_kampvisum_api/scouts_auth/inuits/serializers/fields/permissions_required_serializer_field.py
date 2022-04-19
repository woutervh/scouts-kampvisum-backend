import copy, inspect

from django.core.exceptions import ValidationError
from rest_framework import serializers


class PermissionRequiredSerializerField(serializers.Field):
    _name = None
    field = None
    permission = None

    def __init__(self, *args, **kwargs):
        self._name = kwargs.pop("name", None)
        self.field = kwargs.pop("field", copy.deepcopy(self.field))
        self.permission = kwargs.pop("permission", None)
        assert self.field is not None, "`field` is a required argument."
        assert not inspect.isclass(self.field), "`field` has not been instantiated."
        assert self.permission is not None, "`permission` is a required argument."
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data: dict) -> dict:
        request = self.context.get("request")
        if not request:
            raise Exception(
                "Make sure request has been given to the context of the serializer,"
                "otherwise PermissionRequiredSerializerField won't work"
            )

        if self.permission and request.user.has_perm(self.permission):
            return data

        raise ValidationError(
            "User {} does not have the required permission ({}) to edit field '{}'".format(
                request.user.username, self.permission, self.name
            )
        )

    def to_representation(self, value):
        request = self.context.get("request")
        if not request:
            raise Exception(
                "Make sure request has been given to the context of the serializer,"
                "otherwise PermissionRequiredSerializerField won't work"
            )

        if self.permission and request.user.has_perm(self.permission):
            return value

        return None

    @property
    def name(self):
        if self._name:
            return self._name

        if hasattr(self, "field_name"):
            return self.field_name

        return "(unknown)"
