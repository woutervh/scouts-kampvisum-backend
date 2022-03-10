from typing import List

from django.conf import settings

from apps.participants.models import VisumParticipant

from apps.visums.models import CampVisum, LinkedParticipantCheck
from apps.visums.models.enums import CheckTypeEnum
from apps.visums.settings import VisumSettings

from scouts_auth.inuits.mail import Email, EmailAttachment, EmailService
from scouts_auth.inuits.utils import TextUtils


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class InuitsVisumMailService(EmailService):
    """
    Prepares visum mails and sends them.

    """

    from_email = VisumSettings.get_email_from()
    template_path_start = settings.RESOURCES_MAIL_TEMPLATE_START
    template_path_end = settings.RESOURCES_MAIL_TEMPLATE_END

    template_id = settings.EMAIL_TEMPLATE

    template_camp_registration = VisumSettings.get_camp_registration_template()

    def notify_responsible_changed(self, check: LinkedParticipantCheck):
        visum: CampVisum = check.sub_category.category.category_set.visum

        checks: List[LinkedParticipantCheck] = LinkedParticipantCheck.objects.get(
            parent__check_type__check_type=CheckTypeEnum.PARTICIPANT_RESPONSIBLE_CHECK,
            sub_category__category__category_set__visum=visum,
        )
        participants: List[VisumParticipant] = []
        for participant_check in checks:
            linked_participants = participant_check.participants.all()
            for linked_participant in linked_participants:
                participants.append(linked_participant)

        logger.debug("Preparing to send mail to")
        dictionary = self._prepare_dictionary_responsible_changed()

    def notify_camp_registered(self, visum: CampVisum):

        dictionary = self._prepare_dictionary_camp_registered(visum=visum)
        recipient = visum.created_by.email
        recipient = VisumSettings.get_camp_registration_notification_to(
            address=recipient, send_to=recipient
        )

        logger.debug(
            "Preparing to send camp registration notification to %s (debug: %s, test: %s, acceptance: %s), using template %s",
            recipient,
            VisumSettings.is_debug(),
            VisumSettings.is_test(),
            VisumSettings.is_acceptance(),
            self.template_camp_registration,
        )

        self._send_prepared_email(
            template_path=self.template_camp_registration,
            dictionary=dictionary,
            subject="Kampregistratie",
            to=recipient,
        )

    def _prepare_dictionary_responsible_changed(self, visum: CampVisum):
        return {
            "registrant__first_name": visum.created_by.first_name,
            "title_mail": "",
        }

    def _prepare_dictionary_camp_registered(self, visum: CampVisum):
        return {
            "registrant__first_name": visum.created_by.first_name,
            "visum_url": VisumSettings.construct_visum_url(visum.id),
            "title_mail": "",
        }

    def _prepare_email_body(self, template_path: str, dictionary: dict) -> str:
        return TextUtils.replace(
            path=template_path,
            dictionary=dictionary,
            placeholder_start="--",
            placeholder_end="--",
        )

    def _send_prepared_email(
        self,
        template_path: str,
        dictionary: dict,
        subject: str,
        to: list = None,
        cc: list = None,
        bcc: list = None,
        reply_to: str = None,
        template_id: str = None,
    ):
        dictionary["title_mail"] = subject

        body = None
        html_body = self._prepare_email_body(
            template_path=template_path, dictionary=dictionary
        )
        html_body = TextUtils.compose_html_email(
            self.template_path_start, html_body, self.template_path_end
        )

        if not reply_to:
            reply_to = self.from_email

        mail = Email(
            subject=dictionary["title_mail"],
            body=body,
            html_body=html_body,
            from_email=self.from_email,
            to=to,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            template_id=template_id,
            is_html=True,
        )

        self.send(mail)
