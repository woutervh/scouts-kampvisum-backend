import logging, uuid

from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.groups.models import (
    ScoutsSectionName,
    ScoutsGroupType,
    DefaultScoutsSectionName,
)


logger = logging.getLogger(__name__)


class DatabaseHelper:
    @receiver(pre_save)
    def set_uuid_on_save(sender, instance, *args, **kwargs):
        if instance.pk is None:
            logger.debug(
                "Generating UUID for DefaultScoutsSectionName fixture (sender: %s, instance: %s)",
                sender,
                type(instance).__name__,
            )

            if (
                not isinstance(instance, DefaultScoutsSectionName)
                and not isinstance(instance, ScoutsGroupType)
                and not isinstance(instance, ScoutsSectionName)
            ):
                return

            try:
                instance = DefaultScoutsSectionName.objects.all().filter(
                    type=kwargs.get("type"), name=kwargs.get("name")
                )

                if instance:
                    return
            except:
                pass

            instance.id = uuid.uuid4()
