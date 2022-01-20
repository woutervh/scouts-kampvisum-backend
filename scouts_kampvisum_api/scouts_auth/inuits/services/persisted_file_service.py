import logging

from django.http import Http404

from scouts_auth.inuits.models import PersistedFile


logger = logging.getLogger(__name__)


class PersistedFileService:
    def save(self, request, **data):
        uploaded_file = data.get("file", None)

        if uploaded_file is None:
            raise Http404("Can't store a non-existent file")

        return self.save_file(
            name=uploaded_file.name,
            content=uploaded_file,
            content_type=uploaded_file.content_type,
        )

    def save_file(
        self, name, content, content_type, instance: PersistedFile = None
    ) -> PersistedFile:
        if not instance:
            instance = PersistedFile()

        instance.file.save(name=name, content=content)
        instance.content_type = content_type

        instance.full_clean()
        instance.save()

        return instance
