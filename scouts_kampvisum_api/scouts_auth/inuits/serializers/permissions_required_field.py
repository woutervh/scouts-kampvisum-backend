import copy, inspect

from rest_framework import serializers


class PermissionRequiredField(serializers.Field):
    field = None
    permission = None

    def __init__(self, *args, **kwargs):
        self.field = kwargs.pop("field", copy.deepcopy(self.field))
        self.permission = kwargs.pop("permission", None)
        assert self.field is not None, "`field` is a required argument."
        assert not inspect.isclass(self.field), "`field` has not been instantiated."
        assert self.permission is not None, "`permission` is a required argument."
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data: dict) -> dict:
        return data

    def to_representation(self, value):
        request = self.context.get("request")
        if not request:
            raise Exception(
                "Make sure request has been given to the context of the serializer,"
                "otherwise PermissionRequiredField won't work"
            )

        if self.permission and request.user.has_perm(self.permission):
            return value

        return None
