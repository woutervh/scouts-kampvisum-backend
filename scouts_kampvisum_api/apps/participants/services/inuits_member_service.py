import logging

from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from apps.participants.models import InuitsMember

from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class InuitsMemberService:

    groupadmin = GroupAdmin()

    def member_create_or_update(
        self,
        inuits_member,
        user: settings.AUTH_USER_MODEL,
        skip_validation: bool = False,
    ):
        try:
            member = InuitsMember.objects.get(
                group_admin_id=inuits_member.group_admin_id
            )

            return self.member_update(
                inuits_member=member,
                updated_inuits_member=inuits_member,
                updated_by=user,
                skip_validation=skip_validation,
            )
        except:
            return self.member_create(
                inuits_member=inuits_member,
                created_by=user,
                skip_validation=skip_validation,
            )

    def _load_scouts_member(
        self, user: settings.AUTH_USER_MODEL, group_admin_id: str
    ) -> InuitsMember:
        scouts_member: AbstractScoutsMember = self.groupadmin.get_member_info(
            active_user=user, group_admin_id=group_admin_id
        )

        if not scouts_member:
            raise ValidationError(
                "Invalid group admin id for member: {}".format(group_admin_id)
            )

        return InuitsMember.from_scouts_member(scouts_member)

    def member_create(
        self,
        inuits_member: InuitsMember,
        created_by: settings.AUTH_USER_MODEL,
        skip_validation: bool = False,
    ) -> InuitsMember:
        # Check if the instance already exists
        existing_member = InuitsMember.objects.safe_get(
            pk=inuits_member.id, group_admin_id=inuits_member.group_admin_id
        )
        if existing_member:
            logger.debug(
                "Found InuitsMember with id %s, not creating",
                inuits_member.id,
            )
            return existing_member

        logger.debug(
            "Creating InuitsMember with group admin id %s",
            inuits_member.group_admin_id,
        )

        if skip_validation:
            inuits_member = InuitsMember(
                group_admin_id=inuits_member.group_admin_id,
                first_name=inuits_member.first_name,
                last_name=inuits_member.last_name,
                email=inuits_member.email,
                birth_date=inuits_member.birth_date,
            )
        else:
            inuits_member = self._load_scouts_member(
                user=created_by, group_admin_id=inuits_member.group_admin_id
            )

        inuits_member.created_by = created_by

        inuits_member.full_clean()
        inuits_member.save()

        return inuits_member

    def member_update(
        self,
        *,
        inuits_member: InuitsMember,
        updated_inuits_member: InuitsMember,
        updated_by: settings.AUTH_USER_MODEL,
        skip_validation: bool = False,
    ) -> InuitsMember:
        if inuits_member.equals(updated_inuits_member):
            return updated_inuits_member

        member = self._load_scouts_member(
            user=updated_by, group_admin_id=inuits_member.group_admin_id
        )
        member.id = inuits_member.id
        member.updated_by = updated_by

        member.full_clean()
        member.save()

        return member
