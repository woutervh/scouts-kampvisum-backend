import os, logging

from django.conf import settings
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)


file_upload_allowed_extensions = settings.FILE_UPLOAD_ALLOWED_EXTENSIONS


def validate_file_extension(value):
    extension = os.path.splitext(value.name)[1]

    allowed_extensions = ["." + ext if not ext.startswith(".") else ext for ext in file_upload_allowed_extensions]

    if not extension in allowed_extensions:
        raise ValidationError("File type not supported, only [" + allowed_extensions + "]")
