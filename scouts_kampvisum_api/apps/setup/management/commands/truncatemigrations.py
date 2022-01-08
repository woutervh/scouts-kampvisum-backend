import logging

from django.db import connection
from django.core.management.base import BaseCommand


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Truncates django's migrations table"
    exception = False

    def _drop(self, cursor, table, name=None):
        if name is None:
            name = table
        logger.debug("Dropping table %s", name)
        cursor.execute("DROP TABLE IF EXISTS {} CASCADE".format(table))

    def _drop_all_tables(self, cursor):
        cursor.execute("DROP SCHEMA public CASCADE;")
        cursor.execute("CREATE SCHEMA public;")
        # cursor.execute("GRANT ALL ON SCHEMA public TO postgres;")
        cursor.execute("GRANT ALL ON SCHEMA public to public;")

    def handle(self, *args, **kwargs):

        with connection.cursor() as cursor:
            # self._drop(cursor, "django_migrations")
            # self._drop(cursor, "django_content_type")
            # self._drop(cursor, "django_admin_log")
            # self._drop(cursor, "django_session")
            # self._drop(cursor, "auth_permission")
            # self._drop(cursor, "auth_group_permissions")
            # self._drop(cursor, "auth_group")
            # self._drop(cursor, "scouts_auth_scoutuser_user_permissions")
            # self._drop(cursor, "scouts_auth_scoutuser_groups")
            self._drop_all_tables(cursor)
