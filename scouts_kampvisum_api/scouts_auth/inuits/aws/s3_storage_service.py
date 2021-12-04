import logging

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage

from scouts_auth.inuits.files import StorageService


logger = logging.getLogger(__name__)


class S3StorageService(StorageService, S3Boto3Storage):

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    default_acl = settings.AWS_DEFAULT_ACL
    file_overwrite = settings.AWS_S3_FILE_OVERWRITE

    local_storage = FileSystemStorage()

    # S3Boto3Storage
    # delete(file_path)
    # exists(file_path)
    # listdir(dir_path)
    # size(file_path)
    # get_modified_time(file_path)

    # Storage
    # open(file_path)
    # save(file_path, file_contents)
    # path(file_path)
    # url(file_path)

    def store_file(self, file_path: str, file_contents):
        return super().save(name=file_path, content=file_contents)

    # @TODO remove s3 specific code from this model
    def get_path(self):
        storage = self.file.storage
        if storage.exists(self.file.name):
            return self.file.name

        return self.get_absolute_path()

    def get_absolute_path(self):
        return self.file.path

    def get_file_contents(self, file_src_path: str):
        """Returns the binary contents of a file on S3."""

        try:
            with super().open(file_src_path, "rb") as remote_file:
                remote_file_contents = remote_file.read()

                return remote_file_contents
        except Exception as exc:
            logger.error("An error occurred while fetching file %s from AWS", file_src_path, exc)

    def copy_file(self, file_src_path: str, file_dest_path: str = None):
        """Copies a file on S3 to local storage."""

        logger.debug("Copying file from S3 to local storage: %s", file_src_path)

        if file_dest_path is None:
            file_dest_path = file_src_path

        remote_file_contents = self.get_file_contents(file_src_path)
        self.local_storage.save(file_dest_path, ContentFile(remote_file_contents))

        return self.local_storage.path(file_dest_path)

    # def delete(self, file_path: str, using=None, keep_parents=False):
    #     storage = self.file.storage

    #     if storage.exists(self.file.name):
    #         storage.delete(self.file.name)

    #     super().delete(using=using, keep_parents=keep_parents)
