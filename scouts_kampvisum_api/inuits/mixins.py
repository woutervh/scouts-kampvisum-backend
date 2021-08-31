import logging
from django.db import models
from django.conf import settings
from rest_framework.exceptions import ValidationError


logger = logging.getLogger(__name__)


# Mixins copied from werkwinkel project:
class CreatedByMixin(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Created by",
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True


class AuditTimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Other mixins:
class FlattenMixin(object):
    """
    Flatten nested serializer data by adding a flatten property in Meta

    @see https://stackoverflow.com/a/41418576
    """

    def __init__(self, *args, **kwargs):
        # self.allowed_fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

    def to_representation(self, obj):
        """
        Move fields from nested serializers to root if Meta.flatten is set
        """
        representation = super().to_representation(obj)
        logger.debug("REPRESENTATION: %s", representation)

        if hasattr(self.Meta, 'flatten'):
            for field, serializer_class in self.Meta.flatten:
                serializer = serializer_class(context=self.context)
                objrep = serializer.to_representation(getattr(obj, field))

                for key in objrep:
                    # if key in representation:
                    #     raise ValidationError(
                    #         "A field with name '" + key + "' already exists")
                    # representation[field + "__" + key] = objrep[key]
                    # representation[key] = objrep[key]
                    if not key in representation:
                        representation[key] = objrep[key]

        return representation

    def to_internal_value(self, data):

        # remove flattened nested keys
        nested_fields = {}
        if hasattr(self.Meta, 'flatten'):
            for field, serializer_class in self.Meta.flatten:
                serializer = serializer_class(context=self.context)
                serializer_fields = serializer.Meta.fields
                serializer_internal = {}
                for key in serializer_fields:
                    if key in data:
                        serializer_internal[key] = data.pop(key)
                nested_fields[field] = serializer_internal

        internal_values = super().to_internal_value(data)
        for key in nested_fields:
            internal_values[key] = nested_fields[key]
        logger.debug("INTERNAL VALUES: %s", internal_values)

        return internal_values
