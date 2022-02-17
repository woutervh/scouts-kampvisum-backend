from django.conf import settings
from django.core.exceptions import ValidationError


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
        value = SettingsHelper.get_attribute(attribute_name, attribute_default_value)

        if isinstance(value, str):
            return list(value)
        if isinstance(value, list):
            return value

        raise ValidationError(
            "Expected a list, but got a {}".format(type(value).__class__.__name__)
        )
