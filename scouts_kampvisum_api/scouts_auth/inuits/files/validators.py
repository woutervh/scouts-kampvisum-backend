import os, logging
from typing import List

from django.core.exceptions import ValidationError

from scouts_auth.inuits.files import StorageSettings


logger = logging.getLogger(__name__)


def validate_uploaded_file(value):
    max_file_size = StorageSettings.get_max_file_size()
    configured_allowed_extensions: List[
        str
    ] = StorageSettings.get_allowed_file_extensions()
    if (
        len(configured_allowed_extensions) == 1
        and configured_allowed_extensions[0] == "*"
    ):
        return

    extension = os.path.splitext(value.name)[1].lower()

    allowed_extensions = [
        "." + ext.lower() if not ext.startswith(".") else ext
        for ext in configured_allowed_extensions
    ]

    logger.info(
        "Configured: %s, allowed: %s", configured_allowed_extensions, allowed_extensions
    )

    if not extension in allowed_extensions:
        raise ValidationError(
            "File extensions '{}' not allowed for upload by setting {}, only [{}]".format(
                extension,
                StorageSettings.FILE_UPLOAD_ALLOWED_EXTENSIONS,
                ", ".join(allowed_extensions),
            )
        )

    return
