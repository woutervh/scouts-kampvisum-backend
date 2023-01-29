from django.contrib.contenttypes.models import ContentType

from scouts_auth.inuits.exceptions import DbNotReadyException

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DjangoDbUtil:

    @staticmethod
    def is_initial_db_ready() -> bool:
        try:
            content_type = ContentType.objects.last()

            if content_type:
                return True
        except Exception:
            raise DbNotReadyException(
                "Unable to load authentication groups, database is probably not ready yet"
            )

        return False
