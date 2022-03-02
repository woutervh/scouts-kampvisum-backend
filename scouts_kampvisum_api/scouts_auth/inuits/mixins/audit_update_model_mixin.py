from django.db import models

from scouts_auth.inuits.mixins import UpdatedOnModelMixin, UpdatedByModelMixin


class AuditUpdateModelMixin(UpdatedOnModelMixin, UpdatedByModelMixin, models.Model):
    class Meta:
        abstract = True
