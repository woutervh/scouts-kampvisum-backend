import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, EmailMultiAlternatives
from anymail.message import AnymailMessage

from scouts_auth.inuits.mail import Email

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class EmailService:

    backend = settings.EMAIL_BACKEND

    def validate_email_arguments(
        self,
        from_email: str = None,
        to: list = None,
        cc: list = None,
        bcc: list = None,
        reply_to: str = None,
    ):
        if from_email is None:
            raise ValidationError(
                "An email must have a sender:, 'from_email' is set to None"
            )
        if isinstance(from_email, list):
            if len(from_email) != 1:
                raise ValidationError(
                    "An email can have only 1 sender, currently set to %s",
                    ",".join(from_email),
                )
            else:
                from_email = from_email[0]
        if to is None and cc is None and bcc is None:
            raise ValidationError(
                "An email must have a receiver:, 'to', 'cc' and 'bcc' are set to None"
            )
        if to is None:
            to = []
        if cc is None:
            cc = []
        if bcc is None:
            bcc = []
        if reply_to is None:
            reply_to = to

        logger.debug(
            "VALIDATE (from_email: %s, to: %s, cc: %s, bcc: %s, reply_to: %s)",
            from_email,
            ",".join(to),
            ",".join(cc),
            ",".join(bcc),
            ",".join(reply_to),
        )

        return from_email, to, cc, bcc, reply_to

    def _add_attachments(
        self,
        message: EmailMessage,
        attachment_paths: list = None,
        attachments: list = None,
    ):
        attachment_paths_len = len(attachment_paths)
        if attachment_paths and attachment_paths_len > 0:
            logger.debug("Adding %d attachments to email", attachment_paths_len)
            for attachment_path in attachment_paths:
                message.attach_file(attachment_path)
        attachments_len = len(attachments)
        if attachments and attachments_len > 0:
            logger.debug(
                "Adding %d EmailAttachment instances to email", attachments_len
            )
            for attachment in attachments:
                name, contents = attachment.get_file_and_contents()
                message.attach(os.path.basename(name), contents)

    def send(self, mail: Email):
        """Convenience method to send email using an Email instance."""
        return self.send_email(
            subject=mail.subject,
            body=mail.body,
            html_body=mail.html_body,
            from_email=mail.from_email,
            to=mail.to,
            cc=mail.cc,
            bcc=mail.bcc,
            reply_to=mail.reply_to,
            attachment_paths=mail.attachment_paths,
            template_id=mail.template_id,
            attachments=mail.attachments,
            is_html=mail.is_html,
        )

    def send_email(
        self,
        subject: str = "",
        body: str = "",
        html_body: str = None,
        from_email: str = None,
        to: list = None,
        cc: list = None,
        bcc: list = None,
        reply_to: str = None,
        attachment_paths: list = None,
        attachments: list = None,
        template_id: str = None,
        is_html: bool = False,
    ):
        """Decides wether to send email through the django backend or SendInBlue."""
        logger.debug("Sending mail through backend %s", self.backend)

        if is_html and (not body or len(body.strip()) == 0):
            logger.warn("Requested to send an html email with an empty text body")
            # body = "Please open this mail in a client that supports html email."
            body = html_body

        from_email, to, cc, bcc, reply_to = self.validate_email_arguments(
            from_email, to, cc, bcc, reply_to
        )

        if self.backend == "anymail.backends.sendinblue.EmailBackend":
            return self.send_send_in_blue_email(
                body=body,
                html_body=html_body,
                subject=subject,
                from_email=from_email,
                to=to,
                cc=cc,
                bcc=bcc,
                reply_to=reply_to,
                attachment_paths=attachment_paths,
                attachments=attachments,
                template_id=template_id,
                is_html=is_html,
            )
        else:
            return self.send_django_email(
                body=body,
                html_body=html_body,
                subject=subject,
                from_email=from_email,
                to=to,
                cc=cc,
                bcc=bcc,
                reply_to=reply_to,
                attachment_paths=attachment_paths,
                attachments=attachments,
                is_html=is_html,
            )

    def send_django_email(
        self,
        subject: str = "",
        body: str = "",
        html_body: str = "",
        from_email: str = None,
        to: list = None,
        cc: list = None,
        bcc: list = None,
        reply_to: str = None,
        attachment_paths: list = None,
        attachments: list = None,
        is_html: bool = False,
    ):
        message = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
        )
        if is_html:
            message.attach_alternative(html_body, "text/html")

        self._add_attachments(
            message=message, attachment_paths=attachment_paths, attachments=attachments
        )

        try:
            logger.debug(
                "Sending mail to %s, from %s, with %d attachments",
                message.to,
                message.from_email,
                len(message.attachments),
            )
            message.send()
        except Exception as exc:
            # Actually do something when this fails
            # https://redmine.inuits.eu/issues/83311
            logger.error("Mail could not be sent", exc)

            raise exc

    def send_send_in_blue_email(
        self,
        subject: str = "",
        body: str = "",
        html_body: str = "",
        from_email: str = None,
        to: list = None,
        cc: list = None,
        bcc: list = None,
        reply_to: str = None,
        attachment_paths: list = None,
        attachments: list = None,
        template_id: str = None,
        is_html: bool = False,
    ):
        message = AnymailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to,
            tags=["Schadeclaim"],  # Anymail extra in constructor
        )
        # if is_html:
        #     message.extra_headers["Content-Type"] = "text/html; charset=UTF8"

        self._add_attachments(
            message=message, attachment_paths=attachment_paths, attachments=attachments
        )

        # if template_id:
        #     logger.debug("Using template with id %s for SendInBlue mail", template_id)
        #     message.template_id = template_id

        try:
            message.send()
        except Exception as exc:
            logger.error("Mail could not be sent through SendInBlue", exc)
            raise exc

        # logger.debug("Mail status: %s", message.anymail_status)
        # logger.debug("TYPE: %s", type(message.anymail_status))
