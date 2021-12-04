import logging, os

from django.conf import settings
from django.core.files.storage import Storage


logger = logging.getLogger(__name__)


class StorageService(Storage):
    def store_file(self, file_path: str, file_contents):
        return super().save(name=file_path, content=file_contents)

    def copy_file(self, file_src_path: str, file_dest_path: str):
        pass

    def get_file_contents(self, file_src_path: str):
        contents = None
        with open(file_src_path, "rb") as f:
            contents = f.read()

        return contents

    def copy_file(self, file_src_path: str, file_dest_path: str = None):
        logger.debug("Fetching file from local filesystem to use as e-mail attachment: %s", file_src_path)
        return file_src_path
