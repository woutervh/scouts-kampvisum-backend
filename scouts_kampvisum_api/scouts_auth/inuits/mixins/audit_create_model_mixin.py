from django.db import models

from scouts_auth.inuits.mixins import CreatedOnModelMixin, CreatedByModelMixin


class AuditCreateModelMixin(CreatedOnModelMixin, CreatedByModelMixin, models.Model):
    class Meta:
        abstract = True
