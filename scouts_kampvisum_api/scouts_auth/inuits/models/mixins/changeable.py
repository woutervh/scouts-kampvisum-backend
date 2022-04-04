from django.db import models

from scouts_auth.inuits.models.fields import OptionalCharField


class Changeable(models.Model):
    """Provides a reference to a change handler method (field name: change_handlers)"""

    # References a method in change_notifier.py
    # Contents should be parsed as a list
    change_handlers = OptionalCharField()

    class Meta:
        abstract = True

    def has_change_handlers(self):
        return True if self.change_handlers else False