from scouts_auth.inuits.utils import SettingsHelper


class OIDCSettings(SettingsHelper):
    """Convenience class with static methods to easily distinguish what settings are required for dependent packages."""

    @staticmethod
    def get_auth_user_model(default_value=None):
        return SettingsHelper.get("AUTH_USER_MODEL", default_value)

    @staticmethod
    def get_authorization_roles_config_package(default_value=None):
        return SettingsHelper.get("AUTHORIZATION_ROLES_CONFIG_PACKAGE", default_value)

    @staticmethod
    def get_authorization_roles_config_yaml(default_value=None):
        return SettingsHelper.get("AUTHORIZATION_ROLES_CONFIG_YAML", default_value)

    @staticmethod
    def get_oidc_op_token_endpoint(default_value=None):
        return SettingsHelper.get("OIDC_OP_TOKEN_ENDPOINT", default_value)

    @staticmethod
    def get_oidc_op_user_endpoint(default_value=None):
        return SettingsHelper.get("OIDC_OP_USER_ENDPOINT", default_value)

    @staticmethod
    def get_oidc_rp_client_id(default_value=None):
        return SettingsHelper.get("OIDC_RP_CLIENT_ID", default_value)

    @staticmethod
    def get_oidc_rp_client_secret(default_value=None):
        return SettingsHelper.get("OIDC_RP_CLIENT_SECRET", default_value)

    @staticmethod
    def get_oidc_verify_ssl(default_value=None):
        return SettingsHelper.get("OIDC_VERIFY_SSL", default_value)

    @staticmethod
    def get_oidc_timeout(default_value=None):
        return SettingsHelper.get("OIDC_TIMEOUT", default_value)

    @staticmethod
    def get_oidc_proxy(default_value=None):
        return SettingsHelper.get("OIDC_PROXY", default_value)

    @staticmethod
    def get_profile_refresh_time(default_value=15):
        return SettingsHelper.get_int("PROFILE_REFRESH", default_value)

    @staticmethod
    def get_profile_refresh_groups_time(default_value=15):
        return SettingsHelper.get_int("PROFILE_REFRESH_GROUPS", default_value)

    @staticmethod
    def get_profile_refresh_functions_time(default_value=15):
        return SettingsHelper.get_int("PROFILE_REFRESH_FUNCTIONS", default_value)

    @staticmethod
    def get_secret_key(default_value=None):
        return SettingsHelper.get("SECRET_KEY", default_value)
