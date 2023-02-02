import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

from scouts_auth.inuits.models.fields import OptionalEmailField


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class User(AbstractUser):
    #
    # PRIMARY KEY (uuid)
    #
    id = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4, unique=True
    )

    #
    # Fields inherited from django.contrib.auth.models.AbstractUser
    #
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[UnicodeUsernameValidator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = OptionalEmailField(blank=True)
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    date_joined = models.DateTimeField(default=timezone.now)

    #
    # Fields inherited from django.contrib.auth.AbstractBaseUser
    #
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return (
            f"id({str(self.id)}), "
            f"username({str(self.username)}), "
            f"first_name({str(self.first_name)}), "
            f"last_name({str(self.last_name)}), "
            f"email({str(self.email)}), "
            f"is_staff({str(self.is_staff)}), "
            f"is_active({str(self.is_active)}), "
            f"date_joined({str(self.date_joined)}), "
            f"last_login({str(self.last_login)}), "
            f"is_superuser({str(self.is_superuser)}), "
            f"groups({', '.join([group.name for group in self.groups]) if self.groups and isinstance(self.groups, list) else '[]'}), "
            f"user_permissions({', '.join(self.user_permissions) if self.user_permissions and isinstance(self.user_permissions, list) else '[]'})"
        )
