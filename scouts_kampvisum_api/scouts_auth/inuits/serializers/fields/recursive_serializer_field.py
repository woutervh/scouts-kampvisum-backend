from rest_framework import serializers


class RecursiveSerializerField(serializers.Serializer):
    """
    Utility class that allows serialization of self-referencing classes.
    """

    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data
