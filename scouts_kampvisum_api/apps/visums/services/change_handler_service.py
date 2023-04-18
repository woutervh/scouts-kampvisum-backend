import datetime
from typing import List, Tuple

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from scouts_auth.groupadmin.settings import GroupAdminSettings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ChangeHandlerService:

    default_change_handler = settings.CHECK_CHANGED

    def handle_changes(self, change_handlers: str, request=None, instance=None):
        change_handlers: List[str] = change_handlers.split(",")

        for change_handler in change_handlers:
            if not hasattr(self, change_handler):
                raise ValidationError(
                    "A change handler was defined ({}), but the method is not defined".format(
                        change_handler
                    )
                )
            logger.debug(
                "Handling change for instance %s (%s) with change_handler %s",
                type(instance).__name__,
                instance.id,
                change_handler,
            )
            getattr(self, change_handler)(request=request, instance=instance)

    # def default_check_changed(self, instance: LinkedCheck):
    def default_check_changed(
        self,
        request,
        instance,
        before_camp_registration_deadline: bool = False,
        now: datetime.datetime = None,
        trigger: bool = False,
    ):
        print("START OF FUNCTIONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
        from apps.visums.models import LinkedCheck
        from apps.deadlines.models import LinkedDeadlineFlag

        visum = None
        is_flag = False
        if isinstance(instance, LinkedCheck):
            print("ISINSTACE1")
            visum = instance.sub_category.category.category_set.visum
        elif isinstance(instance, LinkedDeadlineFlag):
            print("ISINSTACE2")
            is_flag = True
            visum = instance.deadline_item.linked_deadline.visum

        all_deadlines = visum.deadlines.all()
        all_deadline_items = deadline.items.all()
        for deadline in all_deadlines:
            print(f"DEADLINEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE: {deadline}")
            if deadline.parent.is_camp_registration:
                for item in all_deadline_items:
                    print(f"ITEM: {item}")
                    print(f"ITEM_PARENT: {item.parent}")
                    try:
                        print(f"AAAAAAAAAAAAAA: {item.linked_check.id == instance.id}")
                        print(f"INSTACE: {instance.id}")
                        print(f"ITEM.Linked_Check: {item.linked_check.id}")
                    except:
                        pass
                    print(f"BBBBBBBBBBBBBB: {item.linked_sub_category == instance.sub_category}")
                    print(f"ITEM.LINKED_SUBCAT: {item.linked_sub_category}")
                    print(f"INSTACE.SUBCAT: {instance.sub_category}")
                    print(f"CCCCCCCCCCCCCC: {item.flag == instance}")
                    try:
                        item_linked_check_id = item.linked_check.id
                        instance_id = instance.id
                    except:
                        item_linked_check_id = item.linked_check
                        instance_id = instance
                    print(f"NEW_CONDITION: {item_linked_check_id == instance_id}")

                    if (
                        not is_flag
                        and (
                            item.linked_sub_category == instance.sub_category
                            or item_linked_check_id == instance_id
                            or item.flag == instance
                        )
                    ) or (is_flag and item.flag == instance):
                        trigger = True
        print(f"TRIGGER: {trigger}")
        self._check_deadline_complete(
            request=request,
            visum=visum,
            before_camp_registration_deadline=before_camp_registration_deadline,
            now=now,
            trigger=trigger,
        )
        # self._check_camp_visum_complete(request=request, visum=visum)

    # def default_deadline_flag_changed(self, instance: LinkedDeadlineFlag):
    def default_deadline_flag_changed(self, request, instance):
        return self._check_deadline_complete(
            request=request, visum=instance.deadline_item.deadline.visum, trigger=False
        )

    def _check_deadline_complete(
        self,
        request,
        visum,
        before_camp_registration_deadline: bool = False,
        now: datetime.datetime = None,
        trigger: bool = False,
    ):
        print("Start _check_deadline_complete")
        if not trigger:
            logger.debug(
                "Changed instance is not part of a deadline, don't check if a mail needs to be sent"
            )
            return

        from apps.deadlines.services import LinkedDeadlineService

        if LinkedDeadlineService().are_camp_registration_deadline_items_checked(
            visum=visum
        ):
            print("LOG1: LinkedDeadlineService().are_camp_registration_deadline_items_checked()")
            # Set the visum as signable if all required checks are completed
            if not visum.is_signable():
                logger.debug(
                    "Setting CampVisum %s (%s) to state SIGNABLE", visum.name, visum.id)
                from apps.visums.models.enums import CampVisumState
                print("VISUM STATE SIGNABLE")
                visum.state = CampVisumState.SIGNABLE
                visum.updated_by = request.user
                visum.updated_on = timezone.now()

                visum.full_clean()
                visum.save()

            from apps.visums.services import InuitsVisumMailService

            if not now:
                (
                    before_camp_registration_deadline,
                    now,
                ) = self.calculate_camp_registration_deadline()

            logger.debug(
                "CAMP REGISTRATION DEADLINE complete - OK to send registration email (%s deadline)",
                "before" if before_camp_registration_deadline else "after",
            )
            return InuitsVisumMailService().notify_camp_registered(
                request=request,
                visum=visum,
                before_camp_registration_deadline=before_camp_registration_deadline,
                now=now,
            )
        else:
            logger.debug(
                "CAMP REGISTRATION DEADLINE not complete - Not sending mail")

        return False

    def _check_camp_visum_complete(self, request, visum):
        from apps.visums.serializers import CampVisumSerializer
        from apps.visums.models.enums import CheckState, CampVisumState

        print("START _check_camp_visum_complete")
        serializer_data = CampVisumSerializer(
            instance=visum, context={"request": request}
        ).data
        # print(f"SER_DATA: {serializer_data}") # Hrůza obrovská - moc velká
        state = serializer_data.get("category_set").get("state")
        print(f"STATEEEE: {state}")
        if CheckState.is_checked_or_irrelevant(state=state):
            print("YESSSSSSSSSSSSSSSSS1")
            logger.debug("Setting CampVisum %s (%s) to state SIGNABLE (category set state: %s)",
                         visum.name, visum.id, state)
            visum.state = CampVisumState.SIGNABLE
        else:
            print("NOOOOOOOOOOOOOOOOOO1")
            logger.debug("Setting CampVisum %s (%s) to state DATA_REQUIRED (category set state: %s)",
                         visum.name, visum.id, state)
            visum.state = CampVisumState.DATA_REQUIRED

        visum.updated_by = request.user
        visum.updated_on = timezone.now()

        visum.full_clean()
        visum.save()

    # def change_camp_responsible(self, instance: LinkedParticipantCheck):
    def change_camp_responsible(self, request, instance):
        from apps.visums.services import InuitsVisumMailService
        from apps.deadlines.services import LinkedDeadlineService
        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        epoch = GroupAdminSettings.get_responsibility_epoch_date()
        now = timezone.now()
        visum = instance.sub_category.category.category_set.visum
        (
                before_camp_registration_deadline,
                now,
            ) = self.calculate_camp_registration_deadline(now=now)
        print(f"EPOCH1: {epoch}")
        print(f"NOW_DATE: {now.date()}")
        print(epoch < now.date())
        if (
            epoch < now.date()
            and LinkedDeadlineService().are_camp_registration_deadline_items_checked(
                visum=visum
            )
        ):  
            print("Sending_mail_notify_responsible_changed")
            InuitsVisumMailService().notify_responsible_changed(
                check=instance,
                before_camp_registration_deadline=before_camp_registration_deadline,
                now=now,
            )
        # return self.default_check_changed(
        #     request=request,
        #     instance=instance,
        #     before_camp_registration_deadline=before_camp_registration_deadline,
        #     now=now,
        #     #trigger=True,
        # )
        return self._check_deadline_complete(
            request=request,
            visum=visum,
            before_camp_registration_deadline=before_camp_registration_deadline,
            now=now,
            trigger=True,
        )
    

    def change_sleeping_location(self, request, instance):
        (
            before_camp_registration_deadline,
            now,
        ) = self.calculate_camp_registration_deadline()

        return self.default_check_changed(
            request=request,
            instance=instance,
            before_camp_registration_deadline=before_camp_registration_deadline,
            now=now,
            trigger=True,
        )

    def change_camp_dates(self, request, instance):
        (
            before_camp_registration_deadline,
            now,
        ) = self.calculate_camp_registration_deadline()

        return self.default_check_changed(
            request=request,
            instance=instance,
            before_camp_registration_deadline=before_camp_registration_deadline,
            now=now,
            trigger=True,
        )

    def calculate_camp_registration_deadline(
        self, now: datetime.datetime = None
    ) -> Tuple[bool, datetime.datetime]:
        from apps.visums.settings import VisumSettings

        before_camp_registration_deadline = True
        deadline = VisumSettings.get_camp_registration_deadline_date()
        now = now if now else timezone.now()
        if deadline < now.date():
            before_camp_registration_deadline = False

        return (before_camp_registration_deadline, now)

    @staticmethod
    def parse_change_handlers(data: dict) -> str:
        # Add change handlers
        change_handlers: List[str] = data.get("change_handlers", None)
        if not change_handlers:
            change_handlers = [ChangeHandlerService.default_change_handler]
        else:
            results = []
            # change_handlers = change_handlers.split(",")
            for change_handler in change_handlers:
                change_handler = change_handler.strip()
                if not change_handler == ChangeHandlerService.default_change_handler:
                    results.append(change_handler)
            # change_handlers = "{},{}".format(
            # default_change_handler, ",".join(results)
            # )
            change_handlers = results

        return ",".join(change_handlers)
