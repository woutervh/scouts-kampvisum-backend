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

    def purge_expired(self):
        with connections['default'].cursor() as cursor:
            try:
                cursor.execute(
                    f"delete from scouts_auth_scoutsusersession sasus where sasus.expiration <= '{now()}'")
            except Exception as exc:
                raise ScoutsAuthException(
                    f"Unable to purge expired sessions", exc)

    def remove_session_data(self, username: str):
        with connections['default'].cursor() as cursor:
            try:
                cursor.execute(
                    f"delete from scouts_auth_scoutsusersession sasus where sasus.username = '{username}'"
                )
            except Exception as exc:
                raise ScoutsAuthException(
                    f"[{username}] Could not remove session data for user")

    def get_session_data(self, username: str):
        self.purge_expired()
        with connections['default'].cursor() as cursor:
            try:
                cursor.execute(
                    f"select sasus.id, sasus.username, sasus.expiration, sasus.data as data from scouts_auth_scoutsusersession sasus where sasus.username = '{username}' and sasus.expiration > '{now()}' and sasus.data is not null"
                )
                return cursor.fetchone()
            except Exception as exc:
                return None
        return None


class ScoutsUserSession(models.Model):

    objects = ScoutsUserSessionManager()

    username = RequiredCharField()
    expiration = TimezoneAwareDateTimeField()
    data = JSONField(null=True)

    @staticmethod
    def from_session(username: str):
        result = ScoutsUserSession.objects.get_session_data(username=username)

        if result:
            session = ScoutsUserSession()

            session.username = result[1]
            session.expiration = result[2]
            session.data = result[3]

            return session

        return None

    def __str__(self):
        return f"[{self.username}] SESSION expires {self.expiration}"
