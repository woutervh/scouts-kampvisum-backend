from datetime import datetime

from django.db import models, connections
from django.db.models import JSONField
from django.utils.timezone import now, make_aware

from scouts_auth.auth.settings import InuitsOIDCSettings
from scouts_auth.auth.exceptions import ScoutsAuthException
from scouts_auth.groupadmin.models import ScoutsToken
from scouts_auth.inuits.models.fields import RequiredCharField, TimezoneAwareDateTimeField

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsUserSessionQueryset(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ScoutsUserSessionManager(models.Manager):
    def get_queryset(self):
        return ScoutsUserSessionQuerySet(self.model, using=self._db)

    def safe_get(self, username: str):
        with connections['default'].cursor() as cursor:
            try:
                cursor.execute(
                    f"select sasus.id, sasus.username, sasus.expiration, sasus.data as data from scouts_auth_scoutsusersession sasus where sasus.username = '{username}'"
                )
                result = cursor.fetchone()
                if result:
                    token = ScoutsToken()

                    token.username = result[1]
                    token.expiration = result[2]
                    token.data = result[3]

                    return token
                return None
            except Exception:
                return None
        return None

    def purge_expired(self):
        with connections['default'].cursor() as cursor:
            try:
                cursor.execute(
                    f"delete from scouts_auth_scoutsusersession sasus where sasus.expiration <= '{now()}'")
            except Exception as exc:
                raise ScoutsAuthException(
                    f"Unable to purge expired sessions", exc)

    def remove_session_data(self, username: str):
        with connection['default'].cursor() as cursor:
            try:
                cursor.execute(
                    f"delete from scouts_auth_scoutsusersession sasus where sasus.username = '{username}'"
                )
            except Exception as exc:
                raise ScoutsAuthException(
                    f"[{username}] Could not remove session data for user")

    def get_session_data(self, username: str, expiration: datetime):
        self.purge_expired()
        with connections['default'].cursor() as cursor:
            try:
                cursor.execute(
                    f"select sasus.id, sasus.username, sasus.expiration, sasus.data as data from scouts_auth_scoutsusersession sasus where sasus.username = '{username}' and sasus.expiration > '{now()}' and sasus.data is not null"
                )
                result = cursor.fetchone()

                if result:
                    token = ScoutsToken()

                    token.username = result[1]
                    token.expiration = result[2]
                    token.data = result[3]

                    return token
            except Exception as exc:
                return None
        return None


class ScoutsUserSession(models.Model):

    objects = ScoutsUserSessionManager()

    username = RequiredCharField()
    expiration = TimezoneAwareDateTimeField()
    data = JSONField(null=True)
