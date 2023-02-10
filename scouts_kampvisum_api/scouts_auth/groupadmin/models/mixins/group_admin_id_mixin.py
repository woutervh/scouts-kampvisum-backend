from django.db import models

from scouts_auth.groupadmin.models.fields import GroupAdminIdField


class GroupAdminIdMixin(models.Model):

    group = GroupAdminIdField()

    class Meta:
        abstract = True
