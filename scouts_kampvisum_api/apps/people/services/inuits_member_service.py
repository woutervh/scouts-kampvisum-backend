import logging

from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from apps.people.models import InuitsMember

from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class InuitsMemberService:
    def inuits_member_create(
        self,
        inuits_member: InuitsMember,
        created_by: settings.AUTH_USER_MODEL,
    ) -> InuitsMember:
        # Check if the instance already exists
        if inuits_member.has_id():
            logger.debug("Querying for InuitsMember with id %s", inuits_member.id)
            try:
                object = InuitsMember.objects.get(pk=inuits_member.id)
                if object:
                    logger.debug(
                        "Found InuitsMember with id %s, not creating",
                        inuits_member.id,
                    )
                    return inuits_member
            except ObjectDoesNotExist:
                pass

        logger.debug(
            "Creating InuitsMember with name %s %s and group admin id %s",
            inuits_member.first_name,
            inuits_member.last_name,
            inuits_member.group_admin_id,
        )

        if not GroupAdmin().validate_member(
            active_user=created_by,
            group_admin_id=inuits_member.group_admin_id,
        ):
            raise ValidationError(
                "Invalid group admin id for member: {}".format(
                    inuits_member.group_admin_id
                )
            )

        inuits_member = InuitsMember(
            group_admin_id=inuits_member.group_admin_id,
            first_name=inuits_member.first_name,
            last_name=inuits_member.last_name,
        )
        inuits_member.full_clean()
        inuits_member.save()

        return inuits_member

    def inuits_member_update(
        self,
        *,
        inuits_member: InuitsMember,
        updated_inuits_member: InuitsMember,
        updated_by: settings.AUTH_USER_MODEL,
    ) -> InuitsMember:
        if inuits_member.equals(updated_inuits_member):
            return updated_inuits_member

        # Update the InuitsMember instance
        inuits_member.first_name = (
            updated_inuits_member.first_name
            if updated_inuits_member.first_name
            else inuits_member.first_name
        )
        inuits_member.last_name = (
            updated_inuits_member.last_name
            if updated_inuits_member.last_name
            else inuits_member.last_name
        )
        inuits_member.updated_by = updated_by

        inuits_member.full_clean()
        inuits_member.save()

        return inuits_member
