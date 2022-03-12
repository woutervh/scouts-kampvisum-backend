from typing import List

from django.utils import timezone

# from apps.deadlines.models import LinkedDeadlineFlag

# from apps.visums.models import LinkedCheck, LinkedParticipantCheck

from scouts_auth.groupadmin.settings import GroupadminSettings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ChangeHandlerService:

    # mail_service = InuitsVisumMailService()
    
    def handle_changes(self, change_handlers: str, instance=None):
        change_handlers: List[str] = change_handlers.split(",")
        
        for change_handler in change_handlers:
            getattr(self, change_handler)(instance=instance)
    
    # def default_check_changed(self, instance: LinkedCheck):
    def default_check_changed(self, instance):
    
        pass
    
    # def default_deadline_flag_changed(self, instance: LinkedDeadlineFlag):
    def default_deadline_flag_changed(self, instance):
        from apps.deadlines.services import LinkedDeadlineService
        
        if LinkedDeadlineService.are_camp_registration_deadline_items_checked(visum=instance.deadline_item.deadline.visum)
        pass

    # def change_camp_responsible(self, instance: LinkedParticipantCheck):
    def change_camp_responsible(self, instance):
        from apps.visums.services import InuitsVisumMailService
        
        epoch = GroupadminSettings.get_responsibility_epoch_date()
        today = timezone.now().date()

        if today > epoch:
            InuitsVisumMailService().notify_responsible_changed()
