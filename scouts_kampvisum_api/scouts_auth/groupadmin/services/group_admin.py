import requests

from django.conf import settings
from django.http import Http404
from django.utils import timezone

# from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.groupadmin.models import (
    ScoutsAllowedCalls,
    AbstractScoutsFunction,
    AbstractScoutsFunctionDescriptionListResponse,
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
    AbstractScoutsFunctionDescriptionListResponseSerializer,
    AbstractScoutsFunctionListResponseSerializer,
    AbstractScoutsGroupSerializer,
    AbstractScoutsGroupListResponseSerializer,
    AbstractScoutsMemberSearchResponseSerializer,
    AbstractScoutsMemberListResponseSerializer,
    AbstractScoutsMemberSerializer,
    AbstractScoutsMemberFrontendSerializer,
)

from scouts_auth.groupadmin.settings import GroupAdminSettings


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GroupAdmin:

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/
    url_allowed_calls = (
        GroupAdminSettings.get_group_admin_allowed_calls_endpoint() + "/"
    )
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep
    url_groups = GroupAdminSettings.get_group_admin_group_endpoint()
    url_groups_vga = GroupAdminSettings.get_group_admin_group_endpoint() + "/vga"
    url_group = GroupAdminSettings.get_group_admin_group_endpoint() + "/{}"
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie
    url_functions = GroupAdminSettings.get_group_admin_functions_endpoint()
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie?groep={group_group_admin_id_start_fragment}
    url_functions_for_group = (
        GroupAdminSettings.get_group_admin_functions_endpoint() + "?groep={}"
    )
    url_function = GroupAdminSettings.get_group_admin_functions_endpoint() + "/{}"
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/profiel
    url_member_profile = GroupAdminSettings.get_group_admin_profile_endpoint()
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/ledenlijst
    url_member_list = GroupAdminSettings.get_group_admin_member_list_endpoint()
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/ledenlijst/filter/stateless
    url_member_list_filtered = GroupAdminSettings.get_group_admin_member_list_filtered_endpoint()
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}
    url_member_info = (
        GroupAdminSettings.get_group_admin_member_detail_endpoint() + "/{}"
    )
    url_member_medical_flash_card = (
        GroupAdminSettings.get_group_admin_member_detail_endpoint() + "/steekkaart"
    )
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken?query={query}
    url_member_search = (
        GroupAdminSettings.get_group_admin_member_search_endpoint() + "?query={}"
    )
    url_member_search_similar = (
        GroupAdminSettings.get_group_admin_member_search_endpoint()
        + "/gelijkaardig?voornaam={}&achternaam={}"
    )

    def post(self, endpoint: str, payload: dict, active_user: settings.AUTH_USER_MODEL = None) -> str:
        """Post the payload to the specified GA endpoint and returns the response as json_data."""
        # logger.debug(
        #     f"GA: Posting data to endpoint {endpoint}", user=active_user)
        try:
            if active_user:
                now = timezone.now()
                response = requests.post(
                    endpoint,
                    headers={
                        "Authorization": f"Bearer {active_user.access_token}",
                    },
                    json=payload
                )
                logger.debug(
                    f"[TIMING] POST {endpoint.replace(GroupAdminSettings.get_group_admin_base_url(), '')}: {(timezone.now() - now).total_seconds()}", user=active_user)
            else:
                response = requests.post(endpoint, data=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise Http404(
                    f"404 - Unable to post to endpoint {endpoint} with payload {payload}"
                )
            raise error

        return response.json()

    def get(self, endpoint: str, active_user: settings.AUTH_USER_MODEL):
        """Makes a request to the GA with the given url and returns the response as json_data."""
        # logger.debug(f"GA: Fetching data from endpoint {endpoint}")
        try:
            now = timezone.now()
            response = requests.get(
                endpoint,
                headers={
                    "Authorization": f"Bearer {active_user.access_token}"
                },
            )
            logger.debug(
                f"[TIMING] GET {endpoint.replace(GroupAdminSettings.get_group_admin_base_url(), '')}: {(timezone.now() - now).total_seconds()}", user=active_user)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise Http404(
                    f"404 GET - Unable to get data from endpoint {endpoint}"
                )
            # elif error.response.status_code == 401:
            #     raise Http404(
            #         "401 GET - Not authorized to get data from endpoint {}".format(endpoint))
            raise error

        return response.json()

    def ping(self, active_user: settings.AUTH_USER_MODEL) -> bool:
        """Makes a request to the GA with the given url and returns the response as json_data."""
        # logger.debug(f"GA: Fetching data from endpoint {endpoint}")
        logger.debug(f"PINGING GROUP ADMIN")
        try:
            now = timezone.now()
            response = requests.get(
                GroupAdminSettings.get_group_admin_base_url(),
                headers={
                    "Authorization": f"Bearer {active_user.access_token}"
                },
            )
            logger.debug(
                f"[TIMING] PING {endpoint.replace(GroupAdminSettings.get_group_admin_base_url(), '')}: {(timezone.now() - now).total_seconds()}")
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise Http404(
                    f"404 GET - Unable to get data from endpoint {endpoint}"
                )
            # elif error.response.status_code == 401:
            #     raise Http404(
            #         "401 GET - Not authorized to get data from endpoint {}".format(endpoint))
            raise error

        return True

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/
    def get_allowed_calls_raw(self, active_user: settings.AUTH_USER_MODEL) -> str:
        """
        Fetches a list of all groupadmin calls that the authenticated user can make

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#overzicht-overzicht-get
        """
        json_data = self.get(self.url_allowed_calls, active_user)

        logger.info(
            f"GA CALL {self.url_allowed_calls.replace(GroupAdminSettings.get_group_admin_base_url(), '')}: get_allowed_calls", user=active_user)
        #logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    # @swagger_auto_schema(
    #     responses={status.HTTP_200_OK: ScoutsAllowedCallsSerializer},
    # )
    def get_allowed_calls(
        self, active_user: settings.AUTH_USER_MODEL
    ) -> ScoutsAllowedCalls:
        json_data = self.get_allowed_calls_raw(active_user)

        now = timezone.now()
        serializer = ScoutsAllowedCallsSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        allowed_calls: ScoutsAllowedCalls = serializer.save()
        logger.debug(
            f"[TIMING] Serialization: {(timezone.now() - now).total_seconds()}, get_allowed_calls()", user=active_user)

        return allowed_calls

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep
    def get_groups_raw(self, active_user: settings.AUTH_USER_MODEL) -> str:
        """
        Fetches a list of all groups for which the authenticated user has rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groepen-get
        """
        json_data = self.get(self.url_groups, active_user)

        logger.info(
            f"GA CALL {self.url_groups.replace(GroupAdminSettings.get_group_admin_base_url(), '')}: get_groups", user=active_user)
        #logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def get_groups(
        self, active_user: settings.AUTH_USER_MODEL
    ) -> AbstractScoutsGroupListResponse:
        json_data = self.get_groups_raw(active_user)

        now = timezone.now()
        serializer = AbstractScoutsGroupListResponseSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        groups_response: AbstractScoutsGroupListResponse = serializer.save()
        logger.debug(
            f"[TIMING] Serialization: {(timezone.now() - now).total_seconds()}, get_groups()", user=active_user)

        return groups_response

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep/vga
    def get_accountable_groups_raw(self, active_user: settings.AUTH_USER_MODEL) -> str:
        """
        Fetches a list of all groups for which the authenticated user is a groupadmin manager (VGA).

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groepen-get-1
        """
        json_data = self.get(self.url_groups_vga, active_user)

        logger.info(
            f"GA CALL: get_accountable_groups ({self.url_groups_vga})", user=active_user)
        #logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def get_accountable_groups(
        self, active_user: settings.AUTH_USER_MODEL
    ) -> AbstractScoutsGroupListResponse:
        json_data = self.get_accountable_groups_raw(active_user)

        now = timezone.now()
        serializer = AbstractScoutsGroupListResponseSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        groups_response: AbstractScoutsGroupListResponse = serializer.save()
        logger.debug(
            f"[TIMING] Serialization: {(timezone.now() - now).total_seconds()}, get_accountable_groups()", user=active_user)

        return groups_response

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep/{group_group_admin_id}
    def get_group_raw(
        self, active_user: settings.AUTH_USER_MODEL, group_group_admin_id: str
    ) -> str:
        """
        Fetches info of a specific group.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groep-get
        """
        url = self.url_group.format(group_group_admin_id)
        json_data = self.get(url, active_user)

        logger.info(f"GA CALL: get_group ({url})", user=active_user)
        #logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def get_group(
        self, active_user: settings.AUTH_USER_MODEL, group_group_admin_id: str
    ) -> AbstractScoutsGroup:
        if group_group_admin_id is None:
            logger.warn(
                "GA: can't fetch a group without a group admin id", user=active_user)
            return None

        json_data = self.get_group_raw(active_user, group_group_admin_id)

        now = timezone.now()
        serializer = AbstractScoutsGroupSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        group: AbstractScoutsGroup = serializer.save()
        logger.debug(
            f"[TIMING] Serialization: {(timezone.now() - now).total_seconds()}, get_group()", user=active_user)

        if group.group_admin_id != group_group_admin_id:
            logger.warn(
                f"GA: unknown group with group admin id {group_group_admin_id}", user=active_user)
            return None

        return group

    def get_group_serialized(
        self, active_user: settings.AUTH_USER_MODEL, group_group_admin_id: str
    ) -> dict:
        if group_group_admin_id is None:
            return None

        group = self.get_group(
            active_user=active_user, group_group_admin_id=group_group_admin_id
        )

        if not group:
            return None

        now = timezone.now()
        data = AbstractScoutsGroupSerializer(group).data
        logger.debug(
            f"[TIMING] Serialization: {(timezone.now() - now).total_seconds()}, get_group_serialized()", user=active_user)

        return data

    def validate_group(
        self, active_user: settings.AUTH_USER_MODEL, group_group_admin_id: str
    ) -> bool:
        serialized_group = self.get_group_serialized(
            active_user, group_group_admin_id)

        if (
            serialized_group
            and serialized_group.get("group_admin_id") == group_group_admin_id
        ):
            return True

        return False

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie?groep{group_group_admin_id_fragment_start}
    def get_function_descriptions_raw(
        self,
        active_user: settings.AUTH_USER_MODEL,
        group_group_admin_id_fragment: str = None,
    ) -> str:
        """
        Fetches a list of functions of the authenticated user for each group.

        The group number can be a complete number, or the first few characters of the group name.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#functies-functielijst-get
        """
        if group_group_admin_id_fragment:
            url = self.url_functions_for_group.format(
                group_group_admin_id_fragment)
        else:
            url = self.url_functions

        json_data = self.get(url, active_user)

        logger.info(
            f"GA CALL: get_function_descriptions ({url})", user=active_user)
        #logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def get_function_descriptions(
        self,
        active_user: settings.AUTH_USER_MODEL,
        group_group_admin_id_fragment: str = None,
    ) -> AbstractScoutsFunctionDescriptionListResponse:
        json_data = self.get_function_descriptions_raw(
            active_user, group_group_admin_id_fragment
        )

        now = timezone.now()
        serializer = AbstractScoutsFunctionDescriptionListResponseSerializer(
            data=json_data
        )
        serializer.is_valid(raise_exception=True)

        function_response: AbstractScoutsFunctionDescriptionListResponse = (
            serializer.save()
        )
        logger.debug(
            f"[TIMING] Serialization: {(timezone.now() - now).total_seconds()}, get_function_descriptions()", user=active_user)

        return function_response

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie/{function_id}
    def get_function_raw(
        self, active_user: settings.AUTH_USER_MODEL, function_id: str
    ) -> str:
        """
        Fetches info of a specific function.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#functies-functie-get
        """
        url = self.url_function.format(function_id)
        json_data = self.get(url, active_user)

        logger.info(
            f"GA CALL: get_function ({url}) for id {function_id}", user=active_user)
        #logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def get_function(
        self, active_user: settings.AUTH_USER_MODEL, function_id: str
    ) -> AbstractScoutsFunction:
        json_data = self.get_function_raw(active_user, function_id)

        now = timezone.now()
        serializer = AbstractScoutsFunctionSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        scouts_function: AbstractScoutsFunction = serializer.save()
        logger.debug(
            f"[TIMING] Serialization: {(timezone.now() - now).total_seconds()}, get_function()", user=active_user)

        return scouts_function

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/profiel
    def get_member_profile_raw(self, active_user: settings.AUTH_USER_MODEL) -> str:
        """
        Fetches the profile information of the current user.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-lid
        """
        url = self.url_member_profile
        json_data = self.get(url, active_user)

        logger.info(f"GA CALL: get_member_profile ({url})", user=active_user)
        #logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def get_member_profile(
        self, active_user: settings.AUTH_USER_MODEL
    ) -> AbstractScoutsMember:
        json_data = self.get_member_profile_raw(active_user)

        now = timezone.now()
        serializer = AbstractScoutsMemberSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        member: AbstractScoutsMember = serializer.save()
        logger.debug(
            f"[TIMING] Serialization: {(timezone.now() - now).total_seconds()}, get_member_profile()", user=active_user)

        return member

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}
    def get_member_info_raw(
        self, active_user: settings.AUTH_USER_MODEL, group_admin_id: str
    ) -> str:
        """
        Fetches member info for a member for which the authenticated user has read rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-lid-get
        """
        url = self.url_member_info.format(group_admin_id)
        json_data = self.get(url, active_user)

        logger.info(f"GA CALL: get_member_info ({url})", user=active_user)
        #logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def get_member_info(
        self, active_user: settings.AUTH_USER_MODEL, group_admin_id: str
    ) -> AbstractScoutsMember:
        json_data = self.get_member_info_raw(active_user, group_admin_id)

        now = timezone.now()
        serializer = AbstractScoutsMemberSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        member: AbstractScoutsMember = serializer.save()
        logger.debug(
            f"[TIMING] Serialization: {(timezone.now() - now).total_seconds()}, get_member_info()", user=active_user)

        if member.group_admin_id != group_admin_id:
            logger.warn(
                f"GA: Unknown member with group admin id {group_admin_id}", user=active_user)
            return None

        return member

    def get_member_info_serialized(
        self, active_user: settings.AUTH_USER_MODEL, group_admin_id: str
    ) -> AbstractScoutsMember:
        if group_admin_id is None:
            logger.warn(
                "GA: Can't fetch member info without a group admin id", user=active_user)
            return None

        member = self.get_member_info(
            active_user=active_user, group_admin_id=group_admin_id
        )

        if not member:
            return None

        now = timezone.now()
        data = AbstractScoutsMemberFrontendSerializer(member).data
        logger.debug(
            f"[TIMING] Serialization: {(timezone.now() - now).total_seconds()}, get_member_info_serialized()", user=active_user)

        return data

    def validate_member(
        self, active_user: settings.AUTH_USER_MODEL, group_admin_id: str
    ) -> bool:
        serialized_member = self.get_member_info_serialized(
            active_user, group_admin_id)

        if (
            serialized_member
            and serialized_member.get("group_admin_id") == group_admin_id
        ):
            return True

        return False

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}/steekkaart
    def get_member_medical_flash_card(
        self, active_user: settings.AUTH_USER_MODEL, group_admin_id: str
    ) -> str:
        """
        Fetches the medical flash card of a member for which the authenticated user has read rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-individuele-steekkaart-get
        """
        raise NotImplementedError(
            "Fetching the medical flash card of a member has not been implemented yet"
        )

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/ledenlijst
    def get_member_list_raw(
        self, active_user: settings.AUTH_USER_MODEL, offset: int = 0
    ) -> str:
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

        logger.info(
            f"GA CALL: get_member_list ({self.url_member_list})", user=active_user)
        #logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def get_member_list(
        self, active_user: settings.AUTH_USER_MODEL, offset: int = 0
    ) -> AbstractScoutsMemberListResponse:
        json_data = self.get_member_list_raw(active_user, offset)

        now = timezone.now()
        serializer = AbstractScoutsMemberListResponseSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        member_list: AbstractScoutsMemberListResponse = serializer.save()
        logger.debug(
            f"[TIMING] Serialization: {(timezone.now() - now).total_seconds()}, get_member_list()", user=active_user)

        return member_list

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/ledenlijst/filter/stateless
    def get_member_list_filtered_raw(
            self, active_user: settings.AUTH_USER_MODEL, payload: dict, offset: int
    ) -> str:
        url = self.url_member_list_filtered
        if offset:
            url = f"{url}?offset={offset}"
        json_data = self.post(url, payload, active_user)

        logger.info(
            f"GA CALL: get_member_list_filtered ({self.url_member_list_filtered})", user=active_user)
        #logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def get_member_list_filtered(
            self,
            active_user: settings.AUTH_USER_MODEL,
            term: str,
            group_group_admin_id: str = None,
            min_age: int = None,
            max_age: int = None,
            gender: str = None,
            offset: int = 0,
    ) -> AbstractScoutsMemberListResponse:
        payload = {
            "criteria": {},
            "kolommen": [
                "Voornaam",
                "Achternaam",
                "Telefoon",
                "adres",
                "email"
            ]
        }
        if term:
            payload["criteria"]["naamlike"] = term
        if group_group_admin_id:
            payload["criteria"]["groepen"] = [group_group_admin_id]
        if max_age or min_age:
            payload["criteria"]["leeftijd"] = dict()
        if max_age:
            payload["criteria"]["leeftijd"]["jongerdan"] = max_age
        if min_age:
            payload["criteria"]["leeftijd"]["ouderdan"] = min_age
        if gender:
            payload["criteria"]["geslacht"] = gender.lower()
        json_data = self.get_member_list_filtered_raw(
            active_user, payload, offset)

        now = timezone.now()
        serializer = AbstractScoutsMemberSearchResponseSerializer(
            data=json_data)
        serializer.is_valid(raise_exception=True)

        member_list: AbstractScoutsMemberSearchResponse = serializer.save()
        logger.debug(
            f"[TIMING] Serialization: {(timezone.now() - now).total_seconds()}, get_member_list_filtered()", user=active_user)

        return member_list

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken/query={query}
    def search_member_raw(
        self, active_user: settings.AUTH_USER_MODEL, term: str
    ) -> str:
        """
        Fetches a list of members that have info similar to the search term.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#zoeken-zoeken-get
        """
        url = self.url_member_search.format(term)
        json_data = self.get(url, active_user)

        logger.info(f"GA CALL: search_member ({url})", user=active_user)
        #logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def search_member(
        self, active_user: settings.AUTH_USER_MODEL, term: str
    ) -> AbstractScoutsMemberSearchResponse:
        json_data = self.search_member_raw(active_user, term)

        now = timezone.now()
        serializer = AbstractScoutsMemberSearchResponseSerializer(
            data=json_data)
        serializer.is_valid(raise_exception=True)

        member_list: AbstractScoutsMemberSearchResponse = serializer.save()
        logger.debug(
            f"[TIMING] Serialization: {(timezone.now() - now).total_seconds()}, search_member()", user=active_user)

        return member_list

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken/gelijkaardig?voornaam={first_name}&achternaam={last_name}
    def search_similar_member(
        self, active_user: settings.AUTH_USER_MODEL, first_name: str, last_name: str
    ) -> str:
        """
        Fetches a list of members that have a name similar to the first_name and last_name arguments.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#zoeken-gelijkaardig-zoeken-get
        """
        url = self.url_member_search_similar.format(first_name, last_name)
        json_data = self.get(url, active_user)

        logger.info(
            f"GA CALL: search_similar_member ({url})", user=active_user)
        #logger.trace("GA RESPONSE: %s", json_data)

        return json_data
