import logging
from typing import List
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.conf import settings

from scouts_auth.groupadmin.models import (
    AbstractScoutsMember,
    AbstractScoutsMemberSearchResponse,
)
from scouts_auth.groupadmin.services import GroupAdmin
from scouts_auth.groupadmin.utils import SettingsHelper
from scouts_auth.inuits.models import GenderHelper


logger = logging.getLogger(__name__)


class GroupAdminMemberService(GroupAdmin):
    def search_member_filtered(
        self,
        active_user: settings.AUTH_USER_MODEL,
        term: str,
        group_group_admin_id: str = None,
        min_age: int = None,
        max_age: int = None,
        gender: str = None,
        include_inactive: bool = False,
    ) -> List[AbstractScoutsMember]:
        response: AbstractScoutsMemberSearchResponse = self.search_member(
            active_user, term
        )

        logger.debug(
            "GA returned a list of %d member(s) for search term %s",
            len(response.members),
            term,
        )

        if group_group_admin_id:
            members: List[AbstractScoutsMember] = self.search_member_filtered_by_group(
                active_user=active_user,
                response=response,
                group_group_admin_id=group_group_admin_id,
                min_age=min_age,
                max_age=max_age,
                gender=gender,
                include_inactive=include_inactive,
            )
        else:
            members: List[
                AbstractScoutsMember
            ] = self.search_member_filtered_by_activity(
                active_user=active_user,
                response=response,
                min_age=min_age,
                max_age=max_age,
                gender=gender,
                include_inactive=include_inactive,
            )

        logger.debug(
            "Found %d member(s) for search term %s, group_admin_id %s, min_age %s, max_age %s, gender %s and include_inactive %s",
            len(members),
            term,
            group_group_admin_id,
            min_age,
            max_age,
            gender,
            include_inactive,
        )

        return members

    def search_member_filtered_by_group(
        self,
        active_user: settings.AUTH_USER_MODEL,
        response: AbstractScoutsMemberSearchResponse,
        group_group_admin_id: str,
        min_age: int = None,
        max_age: int = None,
        gender: str = None,
        include_inactive: bool = False,
    ) -> List[AbstractScoutsMember]:
        results = []
        for partial_member in response.members:
            member: AbstractScoutsMember = self.get_member_info(
                active_user, partial_member.group_admin_id
            )

            for function in member.functions:
                if function.scouts_group.group_admin_id == group_group_admin_id:
                    results.append(member)
                    break

        return self._apply_additional_filters(
            members=results, min_age=min_age, max_age=max_age, gender=gender
        )

    def search_member_filtered_by_activity(
        self,
        active_user: settings.AUTH_USER_MODEL,
        response: AbstractScoutsMemberSearchResponse,
        min_age: int = None,
        max_age: int = None,
        gender: str = None,
        include_inactive: bool = False,
    ) -> List[AbstractScoutsMember]:
        results = []
        # The "activity epoch" after which a member is deemed a past active member
        activity_epoch = self._calculate_activity_epoch(
            datetime.now(), SettingsHelper.get_activity_epoch()
        )

        for partial_member in response.members:
            member: AbstractScoutsMember = self.get_member_info(
                active_user, partial_member.group_admin_id
            )

            was_active = False
            end_of_activity_period_counter = 0
            for function in member.functions:
                # Member was active in at least one function since the activity epoch, don't look further
                if was_active:
                    break

                end_of_activity_period: datetime = function.end

                # Member has ended an activity for at least one function, examine
                if end_of_activity_period:
                    # An end date of a function was registered in the member record
                    end_of_activity_period_counter = end_of_activity_period_counter + 1

                    logger.debug("DATE: %s", isinstance(end_of_activity_period, date))
                    logger.debug(
                        "DATETIME: %s", isinstance(end_of_activity_period, datetime)
                    )

                    end_of_activity_period = end_of_activity_period.date()

                    # Was the end date of the activity after the activity epoch ?
                    if activity_epoch < end_of_activity_period:
                        # Not all insurance types require recently active members to be included in the search results
                        # (currently only temporary insurance for non-members)
                        was_active = True

                        if include_inactive:
                            member.inactive_member = True
                            results.append(member)

            # The member is still active
            if end_of_activity_period_counter == 0:
                results.append(member)

        return self._apply_additional_filters(
            members=results, min_age=min_age, max_age=max_age, gender=gender
        )

    def _apply_additional_filters(
        self,
        members: List[AbstractScoutsMember],
        min_age: int = None,
        max_age: int = None,
        gender: str = None,
    ) -> List[AbstractScoutsMember]:
        results = []

        if min_age:
            min_age = int(min_age)
        if max_age:
            max_age = int(max_age)
        if gender:
            gender = GenderHelper.parse_gender(gender)

        for member in members:
            older_than_min_age = True
            younger_than_max_age = True
            requested_gender = True

            if min_age or max_age:
                # delta = relativedelta(
                #     datetime.now().date().year, member.birth_date.year
                # ).years
                delta = datetime.now().date().year - member.birth_date.year
                # logger.info(
                #     "DELTA: %s, min_age: %s, max_age: %s", delta, min_age, max_age
                # )

                if min_age:
                    if delta < min_age:
                        # logger.info(
                        #     "Member %s is younger than the minimum age %s (%s)",
                        #     member.email,
                        #     min_age,
                        #     member.birth_date,
                        # )
                        older_than_min_age = False
                if max_age:
                    if delta > max_age:
                        # logger.info(
                        #     "Member %s is older than the maximum age %s (%s)",
                        #     member.email,
                        #     max_age,
                        #     member.birth_date,
                        # )
                        younger_than_max_age = False

            if gender:
                if member.gender != gender:
                    requested_gender = False

            logger.info(
                "MEMBER %s: birth_date: %s -> (older_than_min_age(%s), younger_than_max_age(%s)), gender: %s -> (requested_gender(%s))",
                member.email,
                member.birth_date,
                older_than_min_age,
                younger_than_max_age,
                member.gender,
                requested_gender,
            )

            if older_than_min_age and younger_than_max_age and requested_gender:
                results.append(member)

        return results

    def _calculate_activity_epoch(
        self, current_date: date, number_of_years: int
    ) -> date:
        if number_of_years == 0:
            return datetime.fromtimestamp(0).date()

        return (current_date - timedelta(days=number_of_years * 365)).date()
