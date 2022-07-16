from rest_framework import permissions


class GroupMembershipPermission(permissions.BasePermission):
    """
    Sets permissions based on membership of a scouts group.
    """

    permission_name = None

    def __init__(self, permission_name):
        self.permission_name = permission_name

    def has_permission(self, request, view):
        return request.user.has_perm(self.permission_name)
