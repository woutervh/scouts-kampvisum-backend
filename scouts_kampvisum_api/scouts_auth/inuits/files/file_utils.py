import tempfile


class FileUtils:
    @staticmethod
    def get_temp_file(filename: str):
        return "%s/%s" % (tempfile.gettempdir(), filename)
