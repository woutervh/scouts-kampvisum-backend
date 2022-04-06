import datetime

from django.utils import timezone
from django.core.exceptions import ValidationError

from scouts_auth.inuits.utils import SettingsHelper


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class VisumSettings(SettingsHelper):
    @staticmethod
    def get_home():
        if SettingsHelper.is_acceptance():
            return "https://kamp-acc.scoutsengidsenvlaanderen.be/kamp"

        if SettingsHelper.is_debug():
            return "http://localhost:8040/kamp"

        return "https://kamp.scoutsengidsenvlaanderen.be/kamp"

    @staticmethod
    def construct_visum_url(visum_id):
        return "{}/{}".format(VisumSettings.get_home(), visum_id)

    @staticmethod
    def get_email_from():
        return SettingsHelper.get("EMAIL_FROM")

    @staticmethod
    def get_email_registration_bcc():
        return SettingsHelper.get("EMAIL_REGISTRATION_BCC")

    @staticmethod
    def get_email_registration_subject():
        return SettingsHelper.get("EMAIL_REGISTRATION_SUBJECT")

    @staticmethod
    def get_email_registration_delta() -> int:
        return SettingsHelper.get_int("CAMP_REGISTRATION_MAIL_DELTA")

    @staticmethod
    def get_sendinblue_tags() -> list:
        return SettingsHelper.get_list("SENDINBLUE_MAIL_TAGS", [])

    @staticmethod
    def get_camp_registration_deadline_name():
        return SettingsHelper.get("CAMP_REGISTRATION_DEADLINE_NAME")

    @staticmethod
    def get_camp_registration_deadline():
        # The deadline for camp registrations
        value = SettingsHelper.get("CAMP_REGISTRATION_DEADLINE")
        month, day = value.split("-")

        return (int(month), int(day))

    @staticmethod
    def get_camp_registration_deadline_date():
        month, day = VisumSettings.get_camp_registration_deadline()

        return datetime.datetime(timezone.now().date().year, month, day).date()

    @staticmethod
    def get_camp_registration_before_deadline_template():
        return SettingsHelper.get(
            "RESOURCES_TEMPLATE_CAMP_REGISTRATION_BEFORE_DEADLINE"
        )

    @staticmethod
    def get_camp_registration_after_deadline_template():
        return SettingsHelper.get("RESOURCES_TEMPLATE_CAMP_REGISTRATION_AFTER_DEADLINE")

    @staticmethod
    def get_camp_changed_after_deadline_template():
        return SettingsHelper.get("RESOURCES_TEMPLATE_CAMP_CHANGED_AFTER_DEADLINE")

    @staticmethod
    def get_camp_registration_notification_to(
        address: str = None, send_to: str = None, label: str = None
    ) -> str:
        """
        Determines who the recipient of a camp registration notification is.

        On production: the camp registrant
        On acceptance: the camp registrant
        On development: the debug address
        """
        processed_address = address
        debug_address = None

        if SettingsHelper.is_test():
            # When on acceptance, send everything to the registrant
            if SettingsHelper.is_acceptance():
                if not send_to:
                    raise ValidationError("Registrant email is not set")
                processed_address = send_to
            else:
                debug_address = SettingsHelper.get("EMAIL_DEBUG_RECIPIENT", None)
                if not debug_address:
                    raise ValidationError("EMAIL_DEBUG_RECIPIENT is not set !")
                processed_address = debug_address
        else:
            if not address:
                raise ValidationError(
                    "Email recipient for camp registration notification is not set"
                )
            processed_address = address

        logger.debug(
            "MAIL (%s) - address: %s, send_to: %s, debug_address: %s, processed_address (actual receiver): %s",
            label if label else "",
            address,
            send_to,
            debug_address,
            processed_address,
        )

        return processed_address
