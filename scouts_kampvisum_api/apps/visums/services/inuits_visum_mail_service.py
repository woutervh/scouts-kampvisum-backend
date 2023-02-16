import datetime
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
    template_camp_changed_after_deadline = (
        VisumSettings.get_camp_changed_after_deadline_template()
    )

    template_camp_responsible_changed_after_deadline = (
        VisumSettings.get_camp_responsible_changed_after_deadline_template()
    )

    def notify_responsible_changed(
        self,
        check: LinkedParticipantCheck,
        before_camp_registration_deadline: bool = False,
        now: datetime.datetime = None,
    ):
        visum: CampVisum = check.sub_category.category.category_set.visum
        delta = VisumSettings.get_email_registration_delta()

        if before_camp_registration_deadline:
            logger.debug(
                "Camp responsible changed - not sending mail because deadline has not yet passed"
            )
            return
        # Only send out 1 email per day for changed checks
        if visum.camp_registration_mail_last_sent:
            time_delta = now - visum.camp_registration_mail_last_sent
            hours = time_delta.days * 24 + time_delta.seconds / 3600

            if hours < delta:
                logger.debug(
                    "Camp responsible changed mail has already been sent today"
                )
                return

        checks: List[
            LinkedParticipantCheck
        ] = LinkedParticipantCheck.objects.all().filter(
            parent__check_type__check_type=CheckTypeEnum.PARTICIPANT_RESPONSIBLE_CHECK,
            sub_category__category__category_set__visum=visum,
        )
        participants: List[VisumParticipant] = []
        for participant_check in checks:
            linked_participants = participant_check.participants.all()
            for linked_participant in linked_participants:
                participants.append(linked_participant)

        dictionary = self._prepare_dictionary_responsible_changed(visum=visum)

        template = self.template_camp_responsible_changed_after_deadline
        to = [participant.participant.email for participant in participants]
        to.append(
            visum.updated_by.email if visum.updated_by else visum.created_by.email
        )
        to = VisumSettings.get_camp_responsible_changed_notification_to(
            addresses=to, label="CAMP REGISTRATION: recipient"
        )

        subject = VisumSettings.get_email_responsible_changed_subject().format(
            visum.name
        )

        logger.debug(
            "Preparing to send camp registration notification to %s (debug: %s, test: %s, acceptance: %s), using template %s and subject %s",
            to,
            VisumSettings.is_debug(),
            VisumSettings.is_test(),
            VisumSettings.is_acceptance(),
            template,
            subject,
        )

        result = self._send_prepared_email(
            template_path=template,
            dictionary=dictionary,
            subject=subject,
            to=to,
        )

    def notify_camp_registered(
        self,
        request,
        visum: CampVisum,
        before_camp_registration_deadline: bool = False,
        now: datetime.datetime = None,
    ):
        """
        Notifies stakeholders about changes to the camp when all camp deadline items have been checked.

        Camp registration complete (all camp registration deadline items checked):
        -> before camp registration deadline: camp_registered_before_deadline.html
        -> after camp registration deadline: camp_registered_after_deadline.html
        If the initial camp registration mail was already sent:
        -> camp_changed_after_deadline.html

        To clarify:
        - Before the camp registration deadline:
          -> emails should be sent once when all the camp registration deadline items have been checked
        - After the camp registration deadline:
          -> emails should be sent when the camp registration deadline items have been checked and on subsequent changes.
             -> If the camp registration mail hasn't been sent yet: the camp registration after deadline mail
             -> If the camp registration mail has already been sent: the camp registration changed mail

        https://redmine.inuits.eu/issues/87010
        https://redmine.inuits.eu/issues/92716
        https://redmine.inuits.eu/issues/92718
        """
        sending_camp_registration_mail = False
        sending_camp_changed_mail = False

        delta = VisumSettings.get_email_registration_delta()

        template = self.template_camp_registration_before_deadline
        subject = VisumSettings.get_email_registration_subject().format(visum.name)
        if before_camp_registration_deadline:
            sending_camp_registration_mail = True

            # Before deadline and camp registration mail has already been sent
            if visum.camp_registration_mail_sent_before_deadline:
                logger.debug("Camp registration mail has already been sent")
                return
        else:
            # After deadline and camp registration mail has not yet been set
            if not visum.camp_registration_mail_sent_after_deadline:
                sending_camp_registration_mail = True
                template = self.template_camp_registration_after_deadline
            # After deadline and camp registration mail has been sent already
            else:
                sending_camp_changed_mail = True
                template = self.template_camp_changed_after_deadline
                subject = VisumSettings.get_email_registration_changed_subject().format(
                    visum.name
                )

        if not sending_camp_registration_mail and sending_camp_changed_mail:
            # Only send out 1 email per day for changed checks
            if visum.camp_registration_mail_last_sent:
                time_delta = now - visum.camp_registration_mail_last_sent
                hours = time_delta.days * 24 + time_delta.seconds / 3600

                if hours < delta:
                    logger.debug(
                        "Camp registration mail has already been sent today")
                    return

        dictionary = self._prepare_dictionary_camp_registered(visum=visum)
        recipient = visum.created_by.email
        recipient = VisumSettings.get_camp_registration_notification_to(
            address=recipient, send_to=recipient, label="CAMP REGISTRATION: recipient"
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
                address=responsible_main,
                send_to=responsible_main,
                label="CAMP REGISTRATION: cc",
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
                address=responsible_adjunct,
                send_to=responsible_adjunct,
                label="CAMP REGISTRATION: cc",
            )
        )

        bcc = []
        bcc.append(
            VisumSettings.get_camp_registration_notification_to(
                address=VisumSettings.get_email_registration_bcc(),
                send_to=VisumSettings.get_email_registration_bcc(),
                label="CAMP REGISTRATION: bcc",
            )
        )
        logger.debug(
            "Preparing to send camp registration notification to %s (debug: %s, test: %s, acceptance: %s), using template %s and subject %s",
            recipient,
            VisumSettings.is_debug(),
            VisumSettings.is_test(),
            VisumSettings.is_acceptance(),
            template,
            subject,
        )

        result = self._send_prepared_email(
            template_path=template,
            dictionary=dictionary,
            subject=subject,
            to=recipient,
            cc=cc,
            bcc=bcc,
        )

        if result:
            if sending_camp_registration_mail:
                if before_camp_registration_deadline:
                    visum.camp_registration_mail_sent_before_deadline = result
                    visum.camp_registration_mail_sent_after_deadline = False
                else:
                    visum.camp_registration_mail_sent_before_deadline = False
                    visum.camp_registration_mail_sent_after_deadline = result

            visum.camp_registration_mail_last_sent = now
            visum.updated_by = request.user
            visum.updated_on = timezone.now()

            visum.full_clean()
            visum.save()

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
    ) -> bool:
        dictionary["title_mail"] = subject
        dictionary["year_footer_mail"] = str(timezone.now().date().year)

        body = None
        html_body = self._prepare_email_body(
            template_path=template_path, dictionary=dictionary
        )
        html_body_end = self._prepare_email_body(
            template_path=self.template_path_end, dictionary=dictionary
        )
        html_body = TextUtils.compose_html_email_prepared_end(
            self.template_path_start, html_body, html_body_end
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

        try:
            self.send(mail)

            return True
        except Exception:
            return False
