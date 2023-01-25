

from django.conf import settings

from scouts_auth.groupadmin.models import AbstractScoutsMember, AbstractScoutsGroupListResponse
from scouts_auth.groupadmin.services import GroupAdminMemberService


class ScoutsUserService:

    group_admin = GroupAdminMemberService()

    def get_scouts_user(self, active_user: settings.AUTH_USER_MODEL):

        # 1) MEMBER PROFILE (rest-ga/lid/profiel)
        # Get the member profile from groepsadmin
        #
        # This contains:
        # - basic user data (username, first_name, phone number, ...)
        # - a list of scouts functions, for a particular group
        user: AbstractScoutsMember = self.group_admin.get_member_profile(
            active_user=active_user)

        # 2) GROUPS (rest-ga/groep)
        # Get the groups that the user has rights to see
        #
        # This list contains:
        # - the group admin id
        # - the name of the group
        groups: AbstractScoutsGroupListResponse = self.group_admin.get_groups(
            active_user=active_user)
