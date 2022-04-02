from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

# from apps.deadlines.models import LinkedDeadlineFlag

# from apps.visums.models import LinkedCheck, LinkedParticipantCheck

from scouts_auth.groupadmin.settings import GroupadminSettings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ChangeHandlerService:

    default_change_handler = settings.CHECK_CHANGED

    # mail_service = InuitsVisumMailService()

    def handle_changes(self, change_handlers: str, instance=None):
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
            getattr(self, change_handler)(instance=instance)

    # def default_check_changed(self, instance: LinkedCheck):
    def default_check_changed(self, instance):
        self._check_deadline_complete(
            visum=instance.sub_category.category.category_set.visum
        )

    # def default_deadline_flag_changed(self, instance: LinkedDeadlineFlag):
    def default_deadline_flag_changed(self, instance):
        self._check_deadline_complete(visum=instance.deadline_item.deadline.visum)

    def _check_deadline_complete(self, visum):
        from apps.deadlines.services import LinkedDeadlineService

        if LinkedDeadlineService().are_camp_registration_deadline_items_checked(
            visum=visum
        ):
            from apps.visums.services import InuitsVisumMailService

            logger.debug("DEADLINE OK - Sending registration email")
            InuitsVisumMailService().notify_camp_registered(visum=visum)
        else:
            logger.debug("DEADLINE NOT OK YET - Not sending mail")

    # def change_camp_responsible(self, instance: LinkedParticipantCheck):
    def change_camp_responsible(self, instance):
        from apps.visums.services import InuitsVisumMailService

        epoch = GroupadminSettings.get_responsibility_epoch_date()
        today = timezone.now().date()

        if today > epoch:
            InuitsVisumMailService().notify_responsible_changed(check=instance)

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
