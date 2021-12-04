import logging, json

from rest_framework import parsers


logger = logging.getLogger(__name__)


class MultipartJsonParser(parsers.MultiPartParser):
    """

    @see https://stackoverflow.com/questions/20473572/django-rest-framework-file-upload/50514022#50514022
    @see https://stackoverflow.com/questions/61161227/uploading-multiple-images-and-nested-json-using-multipart-form-data-in-django-re
    """

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(stream, media_type=media_type, parser_context=parser_context)

        data = {}

        logger.debug("REST API: received frontend input:")

        for file in result.files:
            logger.debug("FILE: %s", result.files.get(file))

        for key, value in result.data.items():
            logger.debug("%s: %s", key, value)

            if type(value) != str:
                data[key] = value
                continue
            if "{" in value or "[" in value:
                try:
                    data[key] = json.loads(value)
                except ValueError:
                    logger.error("Value error while attempting to parse value as json (key: %s)", key)
                    data[key] = value
            else:
                data[key] = value

        return parsers.DataAndFiles(data, result.files)
