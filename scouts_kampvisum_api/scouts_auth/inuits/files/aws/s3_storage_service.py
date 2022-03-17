from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage

from scouts_auth.inuits.files import CustomStorage, StorageSettings

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class S3StorageService(CustomStorage, S3Boto3Storage):

    bucket_name = StorageSettings.get_s3_bucket_name()
    # default_acl = StorageSettings.get_s3_default_acl()
    file_overwrite = StorageSettings.get_s3_file_overwrite()

    local_storage = FileSystemStorage()

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
            logger.error(
                "An error occurred while fetching file %s from AWS", file_src_path, exc
            )

    def copy_file(self, file_src_path: str, file_dest_path: str = None):
        """Copies a file on S3 to local storage."""

        logger.debug("Copying file from S3 to local storage: %s", file_src_path)

        if file_dest_path is None:
            file_dest_path = file_src_path

        remote_file_contents = self.get_file_contents(file_src_path)
        self.local_storage.save(file_dest_path, ContentFile(remote_file_contents))

        return self.local_storage.path(file_dest_path)

    def copy(self, src_bucket, src_key, dst_bucket, dst_key):
        copy_source = {"Bucket": src_bucket, "Key": src_key}
        self.bucket.meta.client.copy(copy_source, dst_bucket, dst_key)

        super().delete(src_key)

        return dst_key

    def rename_file(self, file_src_path: str, file_dest_path: str):
        """
        Renames a file on S3.

        @see https://docs.aws.amazon.com/AmazonS3/latest/userguide/copy-object.html
        """

        self.copy(
            src_bucket=self.bucket_name,
            src_key=file_src_path,
            dst_bucket=self.bucket_name,
            dst_key=file_dest_path,
        )
        super().delete(file_src_path)

        return file_dest_path
