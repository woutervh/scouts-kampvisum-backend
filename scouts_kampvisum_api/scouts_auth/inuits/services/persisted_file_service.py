import os
import uuid
import mimetypes

from django.http import Http404
from django.conf import settings
from django.core.files.base import File
from django.core.exceptions import ValidationError

from scouts_auth.inuits.models import PersistedFile

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class PersistedFileService:
    def save(self, request, data):
        uploaded_file = data.get("file", None)
        uuid_location = data.get("uuid_location", None)
        

        if uploaded_file is None:
            raise Http404(
                f"[{request.user.username}] Can't store a non-existent file")

        return self.save_file(
            name=uploaded_file.name,
            content=uploaded_file,
            content_type=uploaded_file.content_type,
            uuid_location=uuid_location
        )

    def save_file(
        self, name, content, content_type, uuid_location, instance: PersistedFile = None
    ) -> PersistedFile:
        
        if not instance:
            instance = PersistedFile()

        name, extension = os.path.splitext(name)

        instance.original_name = "{}{}".format(name, extension)
        # instance.file.save(
        #     name="{}/{}{}".format(uuid.uuid4(), name, extension),
        #     content=content,
        # )
        logger.debug('INSTANCE FILE UUID: %s', uuid_location)
        instance.id = uuid_location
        instance.content_type = content_type

        instance.full_clean()
        instance.save()
        
        logger.debug('INSTANCE FILE: %s', instance)

        return instance

    def save_local_file(self, path):
        with open(path, "rb") as f:
            upload = File(f)
            mime, encoding = mimetypes.guess_type(path)

            logger.debug("PATH: %s - MIME: %s", path, mime)
            print("PATH: {} - MIME: {}".format(path, mime))
            return self.save_file(name=upload.name, content=upload, content_type=mime)

    def rename(self, file: PersistedFile, new_name: str):
        if not new_name.strip():
            raise ValidationError("New name not set !")

        file.file.copy()
