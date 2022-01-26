import logging

from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from apps.people.models import InuitsNonMember

from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class InuitsNonMemberService:

    groupadmin = GroupAdmin()

    def create_or_update(
        self,
        inuits_non_member,
        user: settings.AUTH_USER_MODEL,
        skip_validation: bool = False,
    ):
        try:
            non_member = InuitsNonMember.objects.get(
                group_group_admin_id=inuits_non_member.group_group_admin_id,
                email=inuits_non_member.email,
            )

            return self.update(
                inuits_non_member=non_member,
                updated_inuits_non_member=inuits_non_member,
                updated_by=user,
                skip_validation=skip_validation,
            )
        except:
            return self.create(
                inuits_non_member=inuits_non_member,
                created_by=user,
                skip_validation=skip_validation,
            )

    def create(
        self,
        inuits_non_member: InuitsNonMember,
        created_by: settings.AUTH_USER_MODEL,
        skip_validation: bool = False,
    ) -> InuitsNonMember:
        # Check if the instance already exists
        if inuits_non_member.has_id():
            logger.debug(
                "Querying for InuitsNonMember with id %s", inuits_non_member.id
            )
            try:
                object = InuitsNonMember.objects.get(pk=inuits_non_member.id)
                if object:
                    logger.debug(
                        "Found InuitsNonMember with id %s, not creating",
                        inuits_non_member.id,
                    )
                    return inuits_non_member
            except ObjectDoesNotExist:
                pass

        logger.debug(
            "Creating InuitsNonMember with name %s %s for group %s",
            inuits_non_member.first_name,
            inuits_non_member.last_name,
            inuits_non_member.group_group_admin_id,
        )

        if not skip_validation:
            if not self.groupadmin.validate_group(
                active_user=created_by,
                group_group_admin_id=inuits_non_member.group_group_admin_id,
            ):
                raise ValidationError(
                    "Invalid group admin id for group: {}".format(
                        inuits_non_member.group_group_admin_id
                    )
                )

        inuits_non_member = InuitsNonMember(
            group_group_admin_id=inuits_non_member.group_group_admin_id,
            first_name=inuits_non_member.first_name,
            last_name=inuits_non_member.last_name,
            phone_number=inuits_non_member.phone_number,
            cell_number=inuits_non_member.cell_number,
            email=inuits_non_member.email,
            birth_date=inuits_non_member.birth_date,
            gender=inuits_non_member.gender,
            street=inuits_non_member.street,
            number=inuits_non_member.number,
            letter_box=inuits_non_member.letter_box,
            postal_code=inuits_non_member.postal_code,
            city=inuits_non_member.city,
            comment=inuits_non_member.comment,
            created_by=created_by,
        )
        inuits_non_member.full_clean()
        inuits_non_member.save()

        return inuits_non_member

    def update(
        self,
        *,
        inuits_non_member: InuitsNonMember,
        updated_inuits_non_member: InuitsNonMember,
        updated_by: settings.AUTH_USER_MODEL,
        skip_validation: bool = False,
    ) -> InuitsNonMember:
        if inuits_non_member.equals(updated_inuits_non_member):
            return updated_inuits_non_member

        # Update the InuitsNonMember instance
        inuits_non_member.group_group_admin_id = (
            updated_inuits_non_member.group_group_admin_id
            if updated_inuits_non_member.group_group_admin_id
            else inuits_non_member.group_group_admin_id
        )
        inuits_non_member.first_name = (
            updated_inuits_non_member.first_name
            if updated_inuits_non_member.first_name
            else inuits_non_member.first_name
        )
        inuits_non_member.last_name = (
            updated_inuits_non_member.last_name
            if updated_inuits_non_member.last_name
            else inuits_non_member.last_name
        )
        inuits_non_member.phone_number = (
            updated_inuits_non_member.phone_number
            if updated_inuits_non_member.phone_number
            else inuits_non_member.phone_number
        )
        inuits_non_member.cell_number = (
            updated_inuits_non_member.cell_number
            if updated_inuits_non_member.cell_number
            else inuits_non_member.cell_number
        )
        inuits_non_member.email = (
            updated_inuits_non_member.email
            if updated_inuits_non_member.email
            else inuits_non_member.email
        )
        inuits_non_member.birth_date = (
            updated_inuits_non_member.birth_date
            if updated_inuits_non_member.birth_date
            else inuits_non_member.birth_date
        )
        inuits_non_member.gender = (
            updated_inuits_non_member.gender
            if updated_inuits_non_member.gender
            else inuits_non_member.gender
        )
        inuits_non_member.street = (
            updated_inuits_non_member.street
            if updated_inuits_non_member.street
            else inuits_non_member.street
        )
        inuits_non_member.number = (
            updated_inuits_non_member.number
            if updated_inuits_non_member.number
            else inuits_non_member.number
        )
        inuits_non_member.letter_box = (
            updated_inuits_non_member.letter_box
            if updated_inuits_non_member.letter_box
            else inuits_non_member.letter_box
        )
        inuits_non_member.postal_code = (
            updated_inuits_non_member.postal_code
            if updated_inuits_non_member.postal_code
            else inuits_non_member.postal_code
        )
        inuits_non_member.city = (
            updated_inuits_non_member.city
            if updated_inuits_non_member.city
            else inuits_non_member.city
        )
        inuits_non_member.comment = (
            updated_inuits_non_member.comment
            if updated_inuits_non_member.comment
            else inuits_non_member.comment
        )
        inuits_non_member.updated_by = updated_by

        inuits_non_member.full_clean()
        inuits_non_member.save()

        return inuits_non_member
