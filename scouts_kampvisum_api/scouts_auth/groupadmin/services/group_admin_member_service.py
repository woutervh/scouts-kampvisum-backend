import logging
from typing import List
from datetime import date, datetime, timedelta

from django.conf import settings

from scouts_auth.groupadmin.models import AbstractScoutsMember, AbstractAbstractScoutsMemberSearchResponse
from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class GroupAdminMemberService(GroupAdmin):
    def search_member_filtered(
        self,
        active_user: settings.AUTH_USER_MODEL,
        term: str,
        group_group_admin_id: str = None,
        include_inactive: bool = False,
    ) -> List[AbstractScoutsMember]:
        response: AbstractAbstractScoutsMemberSearchResponse = self.search_member(active_user, term)

        logger.debug("GA returned a list of %d member(s) for search term %s", len(response.members), term)

        if group_group_admin_id:
            members: List[AbstractScoutsMember] = self.search_member_filtered_by_group(
                active_user, response, group_group_admin_id, include_inactive
            )

            logger.debug(
                "Found %d member(s) for search term %s, group_admin_id %s and include_inactive %s",
                len(members),
                term,
                group_group_admin_id,
                include_inactive,
            )

            return members
        else:
            members: List[AbstractScoutsMember] = self.search_member_filtered_by_activity(
                active_user, response, include_inactive
            )

            logger.debug(
                "Found %d member(s) for search_term %s, group_admin_id %s and include_inactive %s",
                len(members),
                term,
                group_group_admin_id,
                include_inactive,
            )

            return members

    def search_member_filtered_by_group(
        self,
        active_user: settings.AUTH_USER_MODEL,
        response: AbstractAbstractScoutsMemberSearchResponse,
        group_group_admin_id: str,
        include_inactive: bool = False,
    ) -> List[AbstractScoutsMember]:
        results = []
        for partial_member in response.members:
            member: AbstractScoutsMember = self.get_member_info(active_user, partial_member.group_admin_id)

            for function in member.functions:
                if function.scouts_group.group_admin_id == group_group_admin_id:
                    results.append(member)
                    break

        return results

    def search_member_filtered_by_activity(
        self,
        active_user: settings.AUTH_USER_MODEL,
        response: AbstractAbstractScoutsMemberSearchResponse,
        include_inactive: bool = False,
    ) -> List[AbstractScoutsMember]:
        results = []
        # The "activity epoch" after which a member is deemed a past active member
        activity_epoch = self._calculate_activity_epoch(datetime.now(), 3)

        for partial_member in response.members:
            member: AbstractScoutsMember = self.get_member_info(active_user, partial_member.group_admin_id)

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
                    from scouts_auth.inuits.utils import DateUtils

                    logger.debug("DATE: %s", isinstance(end_of_activity_period, date))
                    logger.debug("DATETIME: %s", isinstance(end_of_activity_period, datetime))

                    # end_of_activity_period = DateUtils.datetime_from_isoformat(end_of_activity_period).date()
                    end_of_activity_period = end_of_activity_period.date()

                    # Was the end date of the activity after the activity epoch ?
                    if activity_epoch < end_of_activity_period:
                        # Not all insurance types require recently active members to be included in the search results
                        # (currently only temporary insurance for non-members)
                        was_active = True

                        if include_inactive:
                            results.append(member)

            # The member is still active
            if end_of_activity_period_counter == 0:
                results.append(member)

        return results

    def _calculate_activity_epoch(self, current_date: date, number_of_years: int) -> date:
        return (current_date - timedelta(days=number_of_years * 365)).date()
