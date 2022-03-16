from django.conf import settings
from django.core.exceptions import ValidationError

from scouts_auth.inuits.utils import GlobalSettingsUtil


class SettingsHelper:
    @staticmethod
    def get_attribute(
        attribute_name: str,
        attribute_default_value: any = None,
        module_default_value: any = None,
    ) -> any:
        return getattr(settings, attribute_name, attribute_default_value)

    @staticmethod
    def get(
        attribute_name: str,
        attribute_default_value: str = None,
        module_default_value: str = None,
    ) -> str:
        return str(
            SettingsHelper.get_attribute(attribute_name, attribute_default_value)
        )

    @staticmethod
    def get_bool(
        attribute_name: str,
        attribute_default_value: bool = False,
        module_default_value: bool = None,
    ) -> bool:
        return bool(
            SettingsHelper.get_attribute(attribute_name, attribute_default_value)
        )

    @staticmethod
    def get_int(
        attribute_name: str,
        attribute_default_value: int = -1,
        module_default_value: int = None,
    ) -> int:
        return int(
            SettingsHelper.get_attribute(attribute_name, attribute_default_value)
        )

    @staticmethod
    def get_list(
        attribute_name: str,
        attribute_default_value: list = None,
        module_default_value: list = None,
    ) -> list:
        try:
            value = SettingsHelper.get_attribute(
                attribute_name, attribute_default_value
            )
        except:
            try:
                value = SettingsHelper.get_attribute(
                    attribute_name, module_default_value
                )
            except:
                value = []

        if isinstance(value, str):
            return list(value)
        if isinstance(value, list):
            return value

        raise ValidationError(
            "Expected a list, but got a {}".format(type(value).__class__.__name__)
        )

    @staticmethod
    def is_debug() -> bool:
        return SettingsHelper.get_bool("DEBUG", False)

    @staticmethod
    def is_test() -> bool:
        # return SettingsHelper.is_debug() and GlobalSettingsUtil.is_test
        return SettingsHelper.is_debug()

    @staticmethod
    def is_acceptance() -> bool:
        return SettingsHelper.is_test() and SettingsHelper.get_bool(
            "IS_ACCEPTANCE", False
        )
