from django.core.files.storage import Storage


class CustomStorage(Storage):
    def get_file_contents(self, file_src_path: str):
        """Returns the binary contents of a file."""
        raise NotImplementedError()

    def copy_file(self, file_src_path: str, file_dest_path: str = None):
        """Copies a file."""
        raise NotImplementedError("")
