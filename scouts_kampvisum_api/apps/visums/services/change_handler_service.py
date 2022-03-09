from django.utils import timezone

from apps.visums.models import LinkedParticipantCheck
from apps.visums.services import InuitsVisumMailService

from scouts_auth.groupadmin.settings import GroupadminSettings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ChangeHandlerService:

    mail_service = InuitsVisumMailService()

    def change_camp_responsible(self, instance: LinkedParticipantCheck):
        epoch = GroupadminSettings.get_responsibility_epoch_date()
        today = timezone.now().date()

        if today > epoch:
            self.mail_service.notify_responsible_changed()
