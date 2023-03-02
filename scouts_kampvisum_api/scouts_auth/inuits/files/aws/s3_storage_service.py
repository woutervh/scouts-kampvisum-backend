import uuid
import ntpath

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import boto3, S3Boto3Storage
from botocore.config import Config
from botocore.exceptions import ClientError
from scouts_auth.inuits.files import CustomStorage, StorageSettings

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class S3StorageService(CustomStorage, S3Boto3Storage):

    access_key = StorageSettings.get_s3_access_key()
    access_secret = StorageSettings.get_s3_access_secret()

    bucket_name = StorageSettings.get_s3_bucket_name()
    # default_acl = StorageSettings.get_s3_default_acl()
    file_overwrite = StorageSettings.get_s3_file_overwrite()

    local_storage = FileSystemStorage()

    def _get_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.access_secret,
            endpoint_url='http://localhost:9000',
            config=Config(signature_version="v4"),
        )

    def generate_presigned_url(self, object_name, expiration=3600):
        """Generate a presigned URL to share an S3 object

        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        logger.debug(f"OBJECT NAME: {object_name}")

        # Generate a presigned URL for the S3 object
        s3_client = self._get_client()

        try:
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': self.bucket_name,
                                                                'Key': 'UUID/' + object_name},
                                                        ExpiresIn=expiration)
        except ClientError as e:
            logging.error(e)
            return None

        # The response contains the presigned URL
        return response

    def generate_presigned_url_post(self, object_name, expiration=3600):
        """Generate a presigned URL to upload a file

        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        # logger.debug(f"OBJECT NAME: {object_name}")

        # Generate a presigned URL for the S3 object
        s3_client = self._get_client()
        try:
            directory_path = str(uuid.uuid4())
            response = s3_client.generate_presigned_post(
                Bucket=self.bucket_name,
                Key=directory_path + '/' + object_name,
                ExpiresIn=expiration
            )

            response['original_name'] = object_name
            response['directory_path'] = directory_path

            # The response contains the presigned URL
            return response
        except ClientError as e:
            logging.error(e)
            return None

        return None

    # @TODO remove s3 specific code from this model
    def get_path(self):
        storage = self.file.storage
        if storage.exists(self.file.name):
            return self.file.name

        return self.get_absolute_path()

    def get_absolute_path(self):
        return self.file.path

    def construct_file_path(self, path):
        dir = ntpath.dirname(path)
        file = ntpath.basename(path)
        return "{}/{}".format(self._normalize_name(self._clean_name(dir)), file)

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

        logger.debug(
            "Copying file from S3 to local storage: %s", file_src_path)

        if file_dest_path is None:
            file_dest_path = file_src_path

        remote_file_contents = self.get_file_contents(file_src_path)
        self.local_storage.save(
            file_dest_path, ContentFile(remote_file_contents))

        return self.local_storage.path(file_dest_path)

    def copy(self, src_bucket, src_key, dst_bucket, dst_key):
        src_key = self.construct_file_path(src_key)
        dst_key = self.construct_file_path(dst_key)

        logger.debug(
            "Copying file %s (bucket: %s)(arg: src_bucket(%s), src_key(%s), dst_bucket(%s), dst_key(%s)) to %s (bucket: %s)",
            src_key,
            src_bucket,
            dst_key,
            dst_bucket,
        )

        return self.bucket.copy({"Bucket": src_bucket, "Key": src_key}, dst_key)

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

        logger.debug("Removing file %s", file_src_path)
        super().delete(file_src_path)

        return file_dest_path
