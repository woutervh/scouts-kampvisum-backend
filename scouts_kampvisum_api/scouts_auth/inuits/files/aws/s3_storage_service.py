from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import boto3, S3Boto3Storage

from scouts_auth.inuits.files import CustomStorage, StorageSettings

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class S3StorageService(CustomStorage, S3Boto3Storage):

    bucket_name = StorageSettings.get_s3_bucket_name()
    # default_acl = StorageSettings.get_s3_default_acl()
    file_overwrite = StorageSettings.get_s3_file_overwrite()

    # access_id = StorageSettings.get_s3_access_id()
    # access_key = StorageSettings.get_s3_access_key()

    local_storage = FileSystemStorage()

    # @TODO remove s3 specific code from this model
    def get_path(self):
        storage = self.file.storage
        if storage.exists(self.file.name):
            return self.file.name

        return self.get_absolute_path()

    def get_absolute_path(self):
        return self.file.path

    def construct_file_path(self, path):
        return self._normalize_name(self._clean_name(path))

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
        from_path = self.construct_file_path(src_key)
        to_path = self.construct_file_path(dst_key)

        copy_result = self.connection.meta.client.copy_object(
            Bucket=dst_bucket,
            CopySource=src_bucket + "/" + from_path,
            Key=to_path,
        )

        if copy_result["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return True

        return False
        # s3 = boto3.resource(
        #     "s3",
        #     aws_access_key_id=self.access_id,
        #     aws_secret_access_key=self.access_key,
        # )
        # copy_source = {"Bucket": src_bucket, "Key": src_key}
        # # self.bucket.meta.client.copy(copy_source, dst_bucket, dst_key)
        # # s3.meta.client.copy(copy_source, dst_bucket, dst_key)
        # # s3.meta.client.copy(Bucket=dst_bucket, CopySource=copy_source, Key=dst_key)

        # bucket = s3.Bucket(self.bucket_name)
        # bucket.copy(copy_source, dst_key)
        # # super().delete(src_key)
        # # super().delete

        # return dst_key
        # super().Object(self.bucket_name, dst_key).copy_from(CopySource="{}/{}".format(self.bucket_name, src_key))
        # super().Object(self.bucket_name, src_key).delete()

    def rename_file(self, file_src_path: str, file_dest_path: str):
        """
        Renames a file on S3.

        @see https://docs.aws.amazon.com/AmazonS3/latest/userguide/copy-object.html
        """

        logger.debug(
            "Copying file %s (bucket: %s) to %s (bucket: %s)",
            file_src_path,
            self.bucket_name,
            file_dest_path,
            self.bucket_name,
        )
        self.copy(
            src_bucket=self.bucket_name,
            src_key=file_src_path,
            dst_bucket=self.bucket_name,
            dst_key=file_dest_path,
        )

        logger.debug("Removing file %s", file_src_path)
        super().delete(file_src_path)

        return file_dest_path
