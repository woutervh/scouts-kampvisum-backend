import datetime
from typing import List, Tuple

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from scouts_auth.groupadmin.settings import GroupadminSettings


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
    ):
        from apps.visums.models import LinkedCheck
        from apps.deadlines.models import LinkedDeadlineFlag

        visum = None
        if isinstance(instance, LinkedCheck):
            visum = instance.sub_category.category.category_set.visum
        elif isinstance(instance, LinkedDeadlineFlag):
            visum = instance.deadline_item.linked_deadline.visum

        self._check_deadline_complete(
            request=request,
            visum=visum,
            before_camp_registration_deadline=before_camp_registration_deadline,
            now=now,
        )
        self._check_camp_visum_complete(request=request, visum=visum)

    # def default_deadline_flag_changed(self, instance: LinkedDeadlineFlag):
    def default_deadline_flag_changed(self, request, instance):
        return self._check_deadline_complete(
            request=request, visum=instance.deadline_item.deadline.visum
        )

    def _check_deadline_complete(
        self,
        request,
        visum,
        before_camp_registration_deadline: bool = False,
        now: datetime.datetime = None,
    ):
        from apps.deadlines.services import LinkedDeadlineService

        if LinkedDeadlineService().are_camp_registration_deadline_items_checked(
            visum=visum
        ):
            from apps.visums.services import InuitsVisumMailService

            if not now:
                (
                    before_camp_registration_deadline,
                    now,
                ) = self.calculate_camp_registration_deadline()

            logger.debug("DEADLINE OK - Sending registration email")
            return InuitsVisumMailService().notify_camp_registered(
                visum=visum,
                before_camp_registration_deadline=before_camp_registration_deadline,
                now=now,
            )
        else:
            logger.debug("DEADLINE NOT OK YET - Not sending mail")

        return False

    def _check_camp_visum_complete(self, request, visum):
        from apps.visums.serializers import CampVisumSerializer
        from apps.visums.models.enums import CheckState, CampVisumState

        serializer_data = CampVisumSerializer(
            instance=visum, context={"request": request}
        ).data
        state = serializer_data.get("category_set").get("state")

        if CheckState.is_checked_or_irrelevant(state=state):
            visum.state = CampVisumState.SIGNABLE
        else:
            visum.state = CampVisumState.DATA_REQUIRED

        visum.full_clean()
        visum.save()

    # def change_camp_responsible(self, instance: LinkedParticipantCheck):
    def change_camp_responsible(self, request, instance):
        from apps.visums.services import InuitsVisumMailService

        epoch = GroupadminSettings.get_responsibility_epoch_date()
        now = timezone.now()

        if epoch < now.date():
            (
                before_camp_registration_deadline,
                now,
            ) = self.calculate_camp_registration_deadline(now=now)

            InuitsVisumMailService().notify_responsible_changed(
                check=instance,
                before_camp_registration_deadline=before_camp_registration_deadline,
                now=now,
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
