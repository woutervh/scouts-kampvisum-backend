from typing import List

from django.conf import settings
from django.utils import timezone

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

    template_camp_registration_before_deadline = (
        VisumSettings.get_camp_registration_before_deadline_template()
    )
    template_camp_registration_after_deadline = (
        VisumSettings.get_camp_registration_after_deadline_template()
    )

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

        cc = []
        responsible_main = (
            LinkedParticipantCheck.objects.filter(
                sub_category__category__category_set__visum=visum,
                parent__name="members_leaders_responsible_main",
            )
            .first()
            .first()
            .participant.email
        )
        cc.append(
            VisumSettings.get_camp_registration_notification_to(
                address=responsible_main, send_to=responsible_main
            )
        )
        responsible_adjunct = (
            LinkedParticipantCheck.objects.filter(
                sub_category__category__category_set__visum=visum,
                parent__name="members_leaders_responsible_adjunct",
            )
            .first()
            .first()
            .participant.email
        )
        cc.append(
            VisumSettings.get_camp_registration_notification_to(
                address=responsible_adjunct, send_to=responsible_adjunct
            )
        )

        template = self.template_camp_registration_before_deadline
        if VisumSettings.get_camp_registration_deadline_date() >= timezone.now().date():
            template = self.template_camp_registration_after_deadline

        logger.debug(
            "Preparing to send camp registration notification to %s (debug: %s, test: %s, acceptance: %s), using template %s",
            recipient,
            VisumSettings.is_debug(),
            VisumSettings.is_test(),
            VisumSettings.is_acceptance(),
            template,
        )

        self._send_prepared_email(
            template_path=template,
            dictionary=dictionary,
            subject=VisumSettings.get_email_registration_subject().format(
                visum.camp.name
            ),
            to=recipient,
            cc=cc,
            bcc=VisumSettings.get_email_registration_bcc(),
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
            tags=VisumSettings.get_sendinblue_tags(),
        )

        self.send(mail)
