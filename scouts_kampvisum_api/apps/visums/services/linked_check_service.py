from django.core.exceptions import ValidationError
from django.db import transaction

from apps.participants.models import VisumParticipant
from apps.participants.services import VisumParticipantService

from apps.locations.models import LinkedLocation
from apps.locations.services import CampLocationService

from apps.visums.models import (
    LinkedCheck,
    LinkedSimpleCheck,
    LinkedDateCheck,
    LinkedDurationCheck,
    LinkedLocationCheck,
    LinkedParticipantCheck,
    LinkedFileUploadCheck,
    LinkedCommentCheck,
    LinkedNumberCheck,
)

from apps.signals.services import ChangeHandlerService

from scouts_auth.groupadmin.services import GroupAdminMemberService
from scouts_auth.inuits.models import PersistedFile
from scouts_auth.inuits.services import PersistedFileService
from scouts_auth.inuits.files import StorageService

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedCheckService:

    location_service = CampLocationService()
    persisted_file_service = PersistedFileService()
    storage_service = StorageService()
    participant_service = VisumParticipantService()
    groupadmin = GroupAdminMemberService()
    change_handler_service = ChangeHandlerService()

    def notify_change(self, instance: LinkedCheck, data_changed: bool = False):
        data_changed = True
        if data_changed and instance.parent.has_change_handlers():
            self.change_handler_service.handle_changes(
                change_handlers=instance.parent.change_handlers, instance=instance
            )

        return instance

    def get_simple_check(self, check_id):
        try:
            return LinkedSimpleCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedSimpleCheck.DoesNotExist:
            logger.error("LinkedSimpleCheck with id %s not found", check_id)
            raise ValidationError(
                "LinkedSimplecheck with id {} not found".format(check_id)
            )

    @transaction.atomic
    def update_simple_check(self, instance: LinkedSimpleCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return self.notify_change(instance)

    def get_date_check(self, check_id):
        try:
            return LinkedDateCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedDateCheck.DoesNotExist:
            raise ValidationError(
                "LinkedDateCheck with id {} not found".format(check_id)
            )

    @transaction.atomic
    def update_date_check(self, instance: LinkedDateCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return self.notify_change(instance)

    def get_duration_check(self, check_id):
        try:
            return LinkedDurationCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedDurationCheck.DoesNotExist:
            logger.error("LinkedDurationCheck with id %s not found", check_id)
            raise ValidationError(
                "LinkedDurationCheck with id {} not found".format(check_id)
            )

    @transaction.atomic
    def update_duration_check(self, instance: LinkedDurationCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)

        data_changed = False
        if instance.start_date != start_date or instance.end_date != end_date:
            data_changed = True

        instance.start_date = start_date
        instance.end_date = end_date

        instance.full_clean()
        instance.save()

        return self.notify_change(instance, data_changed=data_changed)

    def get_location_check(self, check_id):
        try:
            return LinkedLocationCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedLocationCheck.DoesNotExist:
            logger.error("LinkedLocationCheck with id %s not found", check_id)
            raise ValidationError(
                "LinkedLocationCheck with id {} not found".format(check_id)
            )

    @transaction.atomic
    def update_location_check(self, request, instance: LinkedLocationCheck, **data):
        return self._update_location(
            request=request, instance=instance, is_camp_location=False, **data
        )

    def get_camp_location_check(self, check_id):
        try:
            return LinkedLocationCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedLocationCheck.DoesNotExist:
            logger.error("LinkedCampLocationCheck with id %s not found", check_id)
            raise ValidationError(
                "LinkedCampLocatonCheck with id {} not found".format(check_id)
            )

    @transaction.atomic
    def update_camp_location_check(
        self, request, instance: LinkedLocationCheck, **data
    ):
        return self._update_location(
            request=request, instance=instance, is_camp_location=True, **data
        )

    @transaction.atomic
    def _update_location(
        self, request, instance: LinkedLocationCheck, is_camp_location=False, **data
    ):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )

        instance.is_camp_location = is_camp_location

        instance.full_clean()
        instance.save()

        logger.debug("DATA: %s", data)

        locations = data.get("locations", [])
        for location in locations:
            linked_location = None
            location_data = {}

            if isinstance(location, LinkedLocation):
                linked_location = location
            else:
                location_data = location

            self.location_service.create_or_update_linked_location(
                request=request,
                instance=linked_location,
                check=instance,
                is_camp_location=is_camp_location,
                **location_data,
            )

        return self.notify_change(instance)

    def get_participant_check(self, check_id):
        try:
            return LinkedParticipantCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedParticipantCheck.DoesNotExist:
            logger.error("LinkedParticipantCheck with id %s not found", check_id)
            raise ValidationError(
                "LinkedParticipantCheck with id {} not found".format(check_id)
            )

    @transaction.atomic
    def update_participant_check(
        self, request, instance: LinkedParticipantCheck, **data
    ):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        data_changed = False

        visum_participants = data.get("participants", [])
        if not visum_participants or len(visum_participants) == 0:
            logger.error("Empty participant list")
            raise ValidationError("Empty participant list")

        if not instance.parent.is_multiple:
            if len(visum_participants) != 1:
                logger.error("This participant list can have only one participant")
                raise ValidationError(
                    "This participant list is limited to 1 participant, {} given as data, {} present on object".format(
                        len(visum_participants), instance.participants.count()
                    )
                )
            existing_visum_participants = instance.participants.all()
            for existing_visum_participant in existing_visum_participants:
                self.unlink_participant(
                    request=request,
                    instance=instance,
                    visum_participant_id=existing_visum_participant.id,
                )
            data_changed = True

        for visum_participant in visum_participants:
            visum_participant = (
                self.participant_service.create_or_update_visum_participant(
                    user=request.user,
                    participant_type=instance.participant_check_type,
                    check=instance,
                    **visum_participant,
                )
            )

            if visum_participant not in instance.participants.all():
                instance.participants.add(visum_participant)

        return self.notify_change(instance=instance, data_changed=data_changed)

    @transaction.atomic
    def toggle_participant_payment_status(
        self, request, instance: LinkedParticipantCheck, visum_participant_id
    ) -> LinkedParticipantCheck:
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        logger.debug("visum participant: %s", visum_participant_id)
        self.participant_service.toggle_payment_status(
            visum_participant_id=visum_participant_id
        )

        return self.notify_change(instance=instance)

    @transaction.atomic
    def unlink_participant(
        self, request, instance: LinkedParticipantCheck, visum_participant_id, **data
    ):
        participant = VisumParticipant.objects.safe_get(id=visum_participant_id)
        if not participant:
            participant = VisumParticipant.objects.safe_get(
                check_id=instance.id,
                inuits_participant_id=visum_participant_id,
                raise_error=True,
            )

        logger.debug(
            "Unlinking participant with id %s from instance with id %s",
            visum_participant_id,
            instance.id,
        )

        if not participant:
            raise ValidationError(
                "Can't unlink: Unknown visum participant with id {}".format(
                    visum_participant_id
                )
            )

        instance.participants.remove(participant)

        instance.full_clean()
        instance.save()

        logger.debug("Deleting VisumParticipant instance with id %s", participant.id)
        participant.delete()

        return self.notify_change(instance)

    def get_file_upload_check(self, check_id):
        try:
            return LinkedFileUploadCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedFileUploadCheck.DoesNotExist:
            logger.error("LinkedFileUploadCheck with id %s not found", check_id)
            raise ValidationError(
                "LinkedFileUploadCheck with id {} not found".format(check_id)
            )

    @transaction.atomic
    def update_file_upload_check(self, instance: LinkedFileUploadCheck, files: list):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )

        if not files or len(files) == 0:
            raise ValidationError("Can't link an empty list of files")

        for file in files:
            new_name = "{}/{}/{}".format(
                instance.sub_category.category.category_set.visum.group.group_admin_id,
                instance.sub_category.category.category_set.visum.camp.name,
                file.original_name,
            )
            logger.debug(
                "FILE: %s (%s) -> new name: %s", file, type(file).__name__, new_name
            )
            renamed_file = self.storage_service.rename_file(
                file_src_path=file.file.name, file_dest_path=new_name
            )

            file.file = renamed_file

            # file.full_clean()
            file.save()

            instance.value.add(file)

        instance.full_clean()
        instance.save()

        return self.notify_change(instance)

    @transaction.atomic
    def unlink_file(
        self, request, instance: LinkedFileUploadCheck, persisted_file_id, **data
    ):
        logger.debug(
            "Unlinking file %s from instance with id %s", persisted_file_id, instance.id
        )
        logger.debug("DATA: %s", data)

        file = PersistedFile.objects.safe_get(id=persisted_file_id)
        if not file:
            raise ValidationError("Unknown file with id {}".format(persisted_file_id))

        instance.value.remove(file)

        instance.full_clean()
        instance.save()

        return self.notify_change(instance)

    def get_comment_check(self, check_id):
        try:
            return LinkedCommentCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedCommentCheck.DoesNotExist:
            logger.error("LinkedCommentCheck with id %s not found", check_id)
            raise ValidationError(
                "LinkedCommentCheck with id {} not found".format(check_id)
            )

    @transaction.atomic
    def update_comment_check(self, instance: LinkedCommentCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return self.notify_change(instance)

    def get_number_check(self, check_id):
        try:
            return LinkedNumberCheck.objects.get(linkedcheck_ptr=check_id)
        except LinkedNumberCheck.DoesNotExist:
            logger.error("LinkedNumberCheck with id %s not found", check_id)
            raise ValidationError(
                "LinkedNumberCheck with id {} not found".format(check_id)
            )

    @transaction.atomic
    def update_number_check(self, instance: LinkedNumberCheck, **data):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )
        instance.value = data.get("value", None)

        instance.full_clean()
        instance.save()

        return self.notify_change(instance)
