from django.urls import path

from scouts_auth.groupadmin.views import (
    ScoutsAllowedCallsView,
    AbstractScoutsFunctionView,
    AbstractScoutsGroupView,
    AbstractScoutsMemberView,
)

view_allowed_calls = ScoutsAllowedCallsView.as_view({"get": "view_allowed_calls"})
view_member_profile_internal = AbstractScoutsMemberView.as_view(
    {"get": "view_member_profile_internal"}
)
view_member_profile = AbstractScoutsMemberView.as_view({"get": "view_member_profile"})
view_member_list = AbstractScoutsMemberView.as_view({"get": "view_member_list"})
view_search_members = AbstractScoutsMemberView.as_view({"get": "search_members"})
view_member_internal = AbstractScoutsMemberView.as_view(
    {"get": "view_member_info_internal"}
)
view_member = AbstractScoutsMemberView.as_view({"get": "view_member_info"})
view_user = AbstractScoutsMemberView.as_view({"get": "view_user"})
view_group_list = AbstractScoutsGroupView.as_view({"get": "view_groups"})
view_accountable_group_list = AbstractScoutsGroupView.as_view(
    {"get": "view_accountable_groups"}
)
view_group = AbstractScoutsGroupView.as_view({"get": "view_group"})
view_functions = AbstractScoutsFunctionView.as_view({"get": "view_functions"})
view_function_list = AbstractScoutsFunctionView.as_view({"get": "view_function_list"})
view_function = AbstractScoutsFunctionView.as_view({"get": "view_function"})

urlpatterns = [
    path("ga/allowed_calls", view_allowed_calls, name="ga_allowed_calls"),
    path("ga/members/list/", view_member_list, name="ga_member_list"),
    path(
        "ga/members/search/<str:term>/", view_search_members, name="ga_search_members"
    ),
    path(
        "ga/members/search/<str:term>/<str:group_group_admin_id>/",
        view_search_members,
        name="ga_search_members_with_group",
    ),
    path(
        "ga/members/info/internal/<str:group_admin_id>",
        view_member_internal,
        name="ga_member_internal",
    ),
    path("ga/members/info/<str:group_admin_id>", view_member, name="ga_member"),
    path(
        "ga/members/profile/internal",
        view_member_profile_internal,
        name="ga_member_profile_internal",
    ),
    path("ga/members/profile", view_member_profile, name="ga_member_profile"),
    path("user", view_user, name="user"),
    path("ga/groups/", view_group_list, name="ga_groups"),
    path("ga/groups/accountable/", view_accountable_group_list, name="ga_groups"),
    path("ga/groups/<str:group_group_admin_id>", view_group, name="ga_group"),
    path("ga/functions", view_functions, name="ga_functions"),
    path(
        "ga/functions/group/<str:group_group_admin_id_fragment>",
        view_function_list,
        name="ga_functions_for_group",
    ),
    path("ga/functions/<str:function_id>", view_function, name="ga_function"),
]
