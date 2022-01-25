import logging

from django.http import Http404

from apps.people.models import InuitsMember
from apps.locations.services import CampLocationService
from apps.visums.models import (
    LinkedCheck,
    LinkedSimpleCheck,
    LinkedDateCheck,
    LinkedDurationCheck,
    LinkedLocationCheck,
    LinkedMemberCheck,
    LinkedParticipantCheck,
    LinkedFileUploadCheck,
    LinkedCommentCheck,
)

from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.services import GroupAdminMemberService
from scouts_auth.inuits.services import PersistedFileService


logger = logging.getLogger(__name__)


class LinkedCheckService:

    location_service = CampLocationService()
    persisted_file_service = PersistedFileService()
    groupadmin = GroupAdminMemberService()

    @staticmethod
    def get_value_type(check: LinkedCheck):
        concrete_type = LinkedCheck.get_concrete_check_type(check.parent)

        check = concrete_type.__class__.objects.get(linkedcheck_ptr=check.id)
        # logger.debug("CONCRETE CHECK: %s", check)

        return check

    def get_simple_check(self, check_id):
        try:
            return LinkedSimpleCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedSimpleCheck.DoesNotExist:
            logger.error("LinkedSimpleCheck with id %s not found", check_id)
            raise Http404

    def update_simple_check(self, instance: LinkedSimpleCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return instance

    def get_date_check(self, check_id):
        try:
            return LinkedDateCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedDateCheck.DoesNotExist:
            raise Http404

    def update_date_check(self, instance: LinkedDateCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return instance

    def get_duration_check(self, check_id):
        try:
            return LinkedDurationCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedDurationCheck.DoesNotExist:
            logger.error("LinkedDurationCheck with id %s not found", check_id)
            raise Http404

    def update_duration_check(self, instance: LinkedDurationCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.start_date = data.get("start_date", None)
        instance.end_date = data.get("end_date", None)

        instance.full_clean()
        instance.save()

        return instance

    def get_location_check(self, check_id):
        try:
            return LinkedLocationCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedLocationCheck.DoesNotExist:
            logger.error("LinkedLocationCheck with id %s not found", check_id)
            raise Http404

    def update_location_check(self, instance: LinkedLocationCheck, **data):
        return self._update_location(instance=instance, is_camp_location=False, **data)

    def get_camp_location_check(self, check_id):
        try:
            return LinkedLocationCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedLocationCheck.DoesNotExist:
            logger.error("LinkedCampLocationCheck with id %s not found", check_id)
            raise Http404

    def update_camp_location_check(self, instance: LinkedLocationCheck, **data):
        return self._update_location(instance=instance, is_camp_location=True, **data)

    def _update_location(
        self, instance: LinkedLocationCheck, is_camp_location=False, **data
    ):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.name = data.get("name", None)
        instance.contact_name = data.get("contact_name", None)
        instance.contact_phone = data.get("contact_phone", None)
        instance.contact_email = data.get("contact_email", None)
        instance.is_camp_location = is_camp_location
        instance.center_latitude = data.get("center_latitude", None)
        instance.center_longitude = data.get("center_longitude", None)
        instance.zoom = data.get("zoom", None)

        instance.full_clean()
        instance.save()

        logger.debug("DATA: %s", data)
        logger.debug("LOCATIONS: %s", data.get("locations", []))
        locations = data.get("locations", [])
        for location in locations:
            logger.debug("LOCATION: %s", location)
            self.location_service.create_or_update(instance=instance, data=location)

        return instance

    def get_member_check(self, check_id):
        try:
            return LinkedMemberCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedMemberCheck.DoesNotExist:
            logger.error("LinkedMemberCheck with id %s not found", check_id)
            raise Http404

    def update_member_check(self, request, instance: LinkedMemberCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        members = data.get("value", [])
        if not members or len(members) == 0:
            logger.error("Empty list of group admin ids")
            raise Http404
        
        for member in members:
            group_admin_id = member.get("group_admin_id", None)
            
            if not group_admin_id:
                logger.error("Expecting a list of dictionaries with 'group_admin_id' set.")
                raise Http404
            
            scouts_member: AbstractScoutsMember = self.groupadmin.get_member_info(active_user=request.user, group_admin_id=group_admin_id)
            inuits_member = InuitsMember.from_scouts_member(scouts_member)
            inuits_member.full_clean()
            inuits_member.save()
            
            instance.value.add(inuits_member)

        instance.full_clean()
        instance.save()        

        return instance

    def unlink_member(self, instance: LinkedMemberCheck, **data):
        logger.debug("Unlinking member from instance with id %s", instance.id)
        logger.debug("DATA: %s", data)

    def get_participant_check(self, check_id):
        try:
            return LinkedParticipantCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedParticipantCheck.DoesNotExist:
            logger.error("LinkedParticipantCheck with id %s not found", check_id)
            raise Http404

    def update_participant_check(self, instance: LinkedParticipantCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.group_admin_id = data.get("start_date", None)
        instance.end_date = data.get("end_date", None)

        instance.full_clean()
        instance.save()

        return instance

    def get_file_upload_check(self, check_id):
        try:
            return LinkedFileUploadCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedFileUploadCheck.DoesNotExist:
            logger.error("LinkedFileUploadCheck with id %s not found", check_id)
            raise Http404

    def update_file_upload_check(self, instance: LinkedFileUploadCheck, uploaded_file):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )

        if uploaded_file is None:
            raise Http404(
                "Can't store a non-existent file (for check {})".format(instance.id)
            )

        file = self.persisted_file_service.save(
            name=uploaded_file.name,
            content=uploaded_file,
            content_type=uploaded_file.content_type,
        )

        instance.value.add(file)

        instance.full_clean()
        instance.save()

        return instance

    def get_comment_check(self, check_id):
        try:
            return LinkedCommentCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedCommentCheck.DoesNotExist:
            logger.error("LinkedCommentCheck with id %s not found", check_id)
            raise Http404

    def update_comment_check(self, instance: LinkedCommentCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return instance
