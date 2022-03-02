from rest_framework import serializers

from scouts_auth.groupadmin.models import AbstractScoutsGroup
from scouts_auth.groupadmin.services import GroupAdmin


import logging

logger = logging.getLogger(__name__)


class AbstractScoutsGroupSerializerField(serializers.Field):
    serialize = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data: any) -> dict:
        logger.debug(
            "Attempting to deserialize scouts group from data of type %s", type(data)
        )

        group_admin_id: str = None
        if isinstance(data, dict):
            logger.trace("DATA: %s", data)
            group_admin_id = data.get(
                "group_group_admin_id", data.get("group_admin_id", None)
            )
        elif isinstance(data, str):
            group_admin_id = data

        if not group_admin_id:
            logger.api("Can't load a group from GroupAdmin without a group admin id")
            return None

        logger.trace("GROUP FIELD data: %s", group_admin_id)
        return GroupAdmin().get_group(
            active_user=self.context.get("request").user,
            group_group_admin_id=group_admin_id,
        )

    def to_representation(self, data: any) -> dict:
        logger.debug(
            "Attempting to serialize scouts group from data of type %s", type(data)
        )

        group_admin_id: str = None
        if isinstance(data, str):
            group_admin_id = data
        elif hasattr(data, "group_group_admin_id"):
            group_admin_id = getattr(data, "group_group_admin_id")
        elif hasattr(data, "group_admin_id"):
            group_admin_id = getattr(data, "group_admin_id")

        if not group_admin_id:
            logger.warn("Can't load a group from GroupAdmin without a group admin id")
            return None

        logger.trace("GROUP FIELD data: %s", group_admin_id)
        group = GroupAdmin().get_group_serialized(
            active_user=self.context.get("request").user,
            group_group_admin_id=group_admin_id,
        )

        return group.get("group_admin_id")

    def validate(self, data: dict) -> AbstractScoutsGroup:
        return AbstractScoutsGroup(**data)
