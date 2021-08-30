import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework import serializers
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE


class BaseModel(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE

    id = models.AutoField(
        primary_key=True, editable=False)
    uuid = models.UUIDField(
        primary_key=False, editable=False, default=uuid.uuid4, unique=True)

    class Meta:
        abstract = True


class RecursiveField(serializers.Serializer):
    """
    Utility class that allows a deserialization of self-referencing classes.
    """

    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(
            instance, context=self.context)
        return serializer.data


@receiver(pre_save, sender=BaseModel)
def set_uuid_on_save(sender, instance, *args, **kwargs):
    if instance.pk is None:
        instance.uuid = uuid.uuid4()
