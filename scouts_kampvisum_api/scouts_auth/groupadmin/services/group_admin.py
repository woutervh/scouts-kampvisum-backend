import logging, requests

from django.conf import settings
from django.http import Http404
from rest_framework import status
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.groupadmin.models import (
    ScoutsAllowedCalls,
    AbstractScoutsFunction,
    AbstractScoutsFunctionListResponse,
    AbstractScoutsGroup,
    AbstractScoutsGroupListResponse,
    AbstractScoutsMemberSearchResponse,
    AbstractScoutsMember,
    AbstractScoutsMemberListResponse,
)
from scouts_auth.groupadmin.serializers import (
    ScoutsAllowedCallsSerializer,
    AbstractScoutsFunctionSerializer,
    AbstractScoutsFunctionListResponseSerializer,
    AbstractScoutsGroupSerializer,
    AbstractScoutsGroupListResponseSerializer,
    AbstractScoutsMemberSearchResponseSerializer,
    AbstractScoutsMemberListResponseSerializer,
    AbstractScoutsMemberSerializer,
    AbstractScoutsMemberFrontendSerializer,
)

from scouts_auth.groupadmin.utils import SettingsHelper


logger = logging.getLogger(__name__)


class GroupAdmin:

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/
    url_allowed_calls = SettingsHelper.get_group_admin_allowed_calls_endpoint() + "/"
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep
    url_groups = SettingsHelper.get_group_admin_group_endpoint()
    url_groups_vga = SettingsHelper.get_group_admin_group_endpoint() + "/vga"
    url_group = SettingsHelper.get_group_admin_group_endpoint() + "/{}"
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie?groep={group_group_admin_id_start_fragment}
    url_functions = SettingsHelper.get_group_admin_functions_endpoint()
    url_functions_for_group = SettingsHelper.get_group_admin_functions_endpoint() + "?groep={}"
    url_function = SettingsHelper.get_group_admin_functions_endpoint() + "/{}"
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/profiel
    url_member_profile = SettingsHelper.get_group_admin_profile_endpoint()
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/ledenlijst
    url_member_list = SettingsHelper.get_group_admin_member_list_endpoint()
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}
    url_member_info = SettingsHelper.get_group_admin_member_detail_endpoint() + "/{}"
    url_member_medical_flash_card = SettingsHelper.get_group_admin_member_detail_endpoint() + "/steekkaart"
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken?query={query}
    url_member_search = SettingsHelper.get_group_admin_member_search_endpoint() + "?query={}"
    url_member_search_similar = (
        SettingsHelper.get_group_admin_member_search_endpoint() + "/gelijkaardig?voornaam={}&achternaam={}"
    )

    def post(self, endpoint: str, payload: dict) -> str:
        """Post the payload to the specified GA endpoint and returns the response as json_data."""
        logger.debug("GA: Posting data to endpoint %s", endpoint)
        try:
            response = requests.post(endpoint, data=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise Http404
            raise error

        return response.json()

    def get(self, endpoint: str, active_user: settings.AUTH_USER_MODEL):
        """Makes a request to the GA with the given url and returns the response as json_data."""
        logger.debug("GA: Fetching data from endpoint %s", endpoint)
        try:
            response = requests.get(endpoint, headers={"Authorization": "Bearer {0}".format(active_user.access_token)})
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise Http404
            raise error

        return response.json()

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/
    def get_allowed_calls_raw(self, active_user: settings.AUTH_USER_MODEL) -> str:
        """
        Fetches a list of all groupadmin calls that the authenticated user can make

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#overzicht-overzicht-get
        """
        json_data = self.get(self.url_allowed_calls, active_user)

        logger.info("GA CALL: %s (%s)", "get_allowed_calls", self.url_allowed_calls)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsAllowedCallsSerializer},
    )
    def get_allowed_calls(self, active_user: settings.AUTH_USER_MODEL) -> ScoutsAllowedCalls:
        json_data = self.get_allowed_calls_raw(active_user)

        serializer = ScoutsAllowedCallsSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        allowed_calls: ScoutsAllowedCalls = serializer.save()

        return allowed_calls

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep
    def get_groups_raw(self, active_user: settings.AUTH_USER_MODEL) -> str:
        """
        Fetches a list of all groups for which the authenticated user has rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groepen-get
        """
        json_data = self.get(self.url_groups, active_user)

        logger.info("GA CALL: %s (%s)", "get_groups", self.url_groups)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_groups(self, active_user: settings.AUTH_USER_MODEL) -> AbstractScoutsGroupListResponse:
        json_data = self.get_groups_raw(active_user)

        serializer = AbstractScoutsGroupListResponseSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        groups_response: AbstractScoutsGroupListResponse = serializer.save()

        return groups_response

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep/vga
    def get_accountable_groups_raw(self, active_user: settings.AUTH_USER_MODEL) -> str:
        """
        Fetches a list of all groups for which the authenticated user is a groupadmin manager (VGA).

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groepen-get-1
        """
        json_data = self.get(self.url_groups_vga, active_user)

        logger.info("GA CALL: %s (%s)", "get_accountable_groups", self.url_groups_vga)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_accountable_groups(self, active_user: settings.AUTH_USER_MODEL) -> AbstractScoutsGroupListResponse:
        json_data = self.get_accountable_groups_raw(active_user)

        serializer = AbstractScoutsGroupListResponseSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        groups_response: AbstractScoutsGroupListResponse = serializer.save()

        return groups_response

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep/{group_group_admin_id}
    def get_group_raw(self, active_user: settings.AUTH_USER_MODEL, group_group_admin_id: str) -> str:
        """
        Fetches info of a specific group.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groep-get
        """
        url = self.url_group.format(group_group_admin_id)
        json_data = self.get(url, active_user)

        logger.info("GA CALL: %s (%s)", "get_group", url)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_group(self, active_user: settings.AUTH_USER_MODEL, group_group_admin_id: str) -> AbstractScoutsGroup:
        if group_group_admin_id is None:
            logger.warn("GA: can't fetch a group without a group admin id")
            return None

        json_data = self.get_group_raw(active_user, group_group_admin_id)

        serializer = AbstractScoutsGroupSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        group: AbstractScoutsGroup = serializer.save()

        return group

    def get_group_serialized(self, active_user: settings.AUTH_USER_MODEL, group_group_admin_id: str) -> dict:
        if group_group_admin_id is None:
            return None

        return AbstractScoutsGroupSerializer(
            self.get_group(active_user=active_user, group_group_admin_id=group_group_admin_id)
        ).data

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie?groep{group_group_admin_id_fragment_start}
    def get_functions_raw(
        self, active_user: settings.AUTH_USER_MODEL, group_group_admin_id_fragment: str = None
    ) -> str:
        """
        Fetches a list of functions of the authenticated user for each group.

        The group number can be a complete number, or the first few characters of the group name.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#functies-functielijst-get
        """
        if group_group_admin_id_fragment:
            url = self.url_functions_for_group.format(group_group_admin_id_fragment)
        else:
            url = self.url_functions

        json_data = self.get(url, active_user)

        logger.info("GA CALL: %s (%s)", "get_functions", url)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_functions(
        self, active_user: settings.AUTH_USER_MODEL, group_group_admin_id_fragment: str = None
    ) -> AbstractScoutsFunctionListResponse:
        json_data = self.get_functions_raw(active_user, group_group_admin_id_fragment)

        serializer = AbstractScoutsFunctionListResponseSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        function_response: AbstractScoutsFunctionListResponse = serializer.save()

        return function_response

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie/{function_id}
    def get_function_raw(self, active_user: settings.AUTH_USER_MODEL, function_id: str) -> str:
        """
        Fetches info of a specific function.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#functies-functie-get
        """
        url = self.url_function.format(function_id)
        json_data = self.get(url, active_user)

        logger.info("GA CALL: %s (%s)", "get_function", url)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_function(self, active_user: settings.AUTH_USER_MODEL, function_id: str) -> AbstractScoutsFunction:
        json_data = self.get_function_raw(active_user, function_id)

        serializer = AbstractScoutsFunctionSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        function: AbstractScoutsFunction = serializer.save()

        return function

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/profiel
    def get_member_profile_raw(self, active_user: settings.AUTH_USER_MODEL) -> str:
        """
        Fetches the profile information of the current user.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-lid
        """
        json_data = self.get(self.url_member_profile, active_user)

        logger.info("GA CALL: %s (%s)", "get_member_profile", self.url_function)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_member_profile(self, active_user: settings.AUTH_USER_MODEL) -> AbstractScoutsMember:
        json_data = self.get_member_profile_raw(active_user)

        serializer = AbstractScoutsMemberSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        member: AbstractScoutsMember = serializer.save()

        return member

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}
    def get_member_info_raw(self, active_user: settings.AUTH_USER_MODEL, group_admin_id: str) -> str:
        """
        Fetches member info for a member for which the authenticated user has read rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-lid-get
        """
        url = self.url_member_info.format(group_admin_id)
        json_data = self.get(url, active_user)

        logger.info("GA CALL: %s (%s)", "get_member_info", url)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_member_info(self, active_user: settings.AUTH_USER_MODEL, group_admin_id: str) -> AbstractScoutsMember:
        json_data = self.get_member_info_raw(active_user, group_admin_id)

        serializer = AbstractScoutsMemberSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        member: AbstractScoutsMember = serializer.save()

        return member

    def get_member_info_serialized(
        self, active_user: settings.AUTH_USER_MODEL, group_admin_id: str
    ) -> AbstractScoutsMember:
        if group_admin_id is None:
            return None

        return AbstractScoutsMemberFrontendSerializer(
            self.get_member_info(active_user=active_user, group_admin_id=group_admin_id)
        ).data

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}/steekkaart
    def get_member_medical_flash_card(self, active_user: settings.AUTH_USER_MODEL, group_admin_id: str) -> str:
        """
        Fetches the medical flash card of a member for which the authenticated user has read rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-individuele-steekkaart-get
        """
        raise NotImplementedError("Fetching the medical flash card of a member has not been implemented yet")

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/ledenlijst
    def get_member_list_raw(self, active_user: settings.AUTH_USER_MODEL, offset: int = 0) -> str:
        """
        Fetches a list of members.

        The number returned is based on server load and current response-time. To fetch
        the remainder of the list, the optional offset parameter can be used.

        The type of list returned is determined by an Accept request header:
        - Accept: */* or Accept: application/json_data returns a json_data list
        - Accept: text/csv returns a csv file
        - Accept: application/pdf returns a pdf file

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#ledenlijst-ledenlijst-get
        """
        json_data = self.get(self.url_member_list, active_user)

        logger.info("GA CALL: %s (%s)", "get_member_list", self.url_member_list)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_member_list(
        self, active_user: settings.AUTH_USER_MODEL, offset: int = 0
    ) -> AbstractScoutsMemberListResponse:
        json_data = self.get_member_list_raw(active_user, offset)

        serializer = AbstractScoutsMemberListResponseSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        member_list: AbstractScoutsMemberListResponse = serializer.save()

        return member_list

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken/query={query}
    def search_member_raw(self, active_user: settings.AUTH_USER_MODEL, term: str) -> str:
        """
        Fetches a list of members that have info similar to the search term.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#zoeken-zoeken-get
        """
        url = self.url_member_search.format(term)
        json_data = self.get(url, active_user)

        logger.info("GA CALL: %s (%s)", "search_member", url)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def search_member(self, active_user: settings.AUTH_USER_MODEL, term: str) -> AbstractScoutsMemberSearchResponse:
        json_data = self.search_member_raw(active_user, term)

        serializer = AbstractScoutsMemberSearchResponseSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        member_list: AbstractScoutsMemberSearchResponse = serializer.save()

        return member_list

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken/gelijkaardig?voornaam={first_name}&achternaam={last_name}
    def search_similar_member(self, active_user: settings.AUTH_USER_MODEL, first_name: str, last_name: str) -> str:
        """
        Fetches a list of members that have a name similar to the first_name and last_name arguments.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#zoeken-gelijkaardig-zoeken-get
        """
        url = self.url_member_search_similar.format(first_name, last_name)
        json_data = self.get(url, active_user)

        logger.info("GA CALL: %s (%s)", "search_similar_member", url)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data
