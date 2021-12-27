from django.conf import settings


class SettingsHelper:
    @staticmethod
    def get_attribute(attribute_name: str, attribute_default_value: any = None) -> any:
        return getattr(settings, attribute_name, attribute_default_value)

    @staticmethod
    def get(attribute_name: str, attribute_default_value: str = None) -> str:
        return str(SettingsHelper.get_attribute(attribute_name, attribute_default_value))

    @staticmethod
    def get_bool(attribute_name: str, attribute_default_value: bool = False) -> bool:
        return bool(SettingsHelper.get_attribute(attribute_name, attribute_default_value))
