from django.core.files.storage import FileSystemStorage

from scouts_auth.inuits.files import CustomStorage

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CustomFileSystemStorage(CustomStorage, FileSystemStorage):
    def __init__(self):
        super().__init__()

    def get_file_contents(self, file_src_path: str):
        if self.is_file_system_storage:
            contents = None
            with open(file_src_path, "rb") as f:
                contents = f.read()

            return contents

        return self.storage.get_file_contents(file_src_path)

    def copy_file(self, file_src_path: str, file_dest_path: str = None):
        logger.debug(
            "Fetching file from local filesystem to use as e-mail attachment: %s",
            file_src_path,
        )
        return file_src_path
