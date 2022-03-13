import datetime

from django.utils import timezone
from django.core.exceptions import ValidationError

from scouts_auth.inuits.utils import SettingsHelper


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
    def get_camp_registration_notification_to(
        address: str = None, send_to: str = None
    ) -> str:
        """
        Determines who the recipient of a camp registration notification is.

        On production: the camp registrant
        On acceptance: the camp registrant
        On development: the debug address
        """
        if SettingsHelper.is_test():
            # When on acceptance, send everything to the registrant
            if SettingsHelper.is_acceptance():
                if not send_to:
                    raise ValidationError("Registrant email is not set")
                return send_to

            address = SettingsHelper.get("EMAIL_DEBUG_RECIPIENT", None)
            if not address:
                raise ValidationError("EMAIL_DEBUG_RECIPIENT is not set !")
            return address

        if not address:
            raise ValidationError(
                "Email recipient for camp registration notification is not set"
            )

        return address
