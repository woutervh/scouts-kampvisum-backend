import logging, importlib

from django.core.files.storage import Storage

from scouts_auth.inuits.files import StorageSettings, CustomStorage


logger = logging.getLogger(__name__)


class StorageService(Storage):

    name = "scouts_auth.inuits.files.StorageService"

    storage = None
    is_file_system_storage = False

    def __init__(self, storage_type: str = None):
        self._load_storage(storage_type)

    def _load_storage(self, storage_type: str = None):
        if not storage_type:
            if StorageSettings.use_s3():
                logger.debug("Storage: using S3")
                storage_type = StorageSettings.get_s3_storage_service_name()
            else:
                logger.debug("Storage: using configured default storage")
                storage_type = StorageSettings.get_default_storage()

                # It should be possible to specify a different DEFAULT_FILE_STORAGE and still use this service
                if storage_type == self.name:
                    storage_type = None

        # If no storage type is configured, use CustomFileSystemStorage
        if not storage_type:
            self.is_file_system_storage = True
            storage_type = "scouts_auth.inuits.files.CustomFileSystemStorage"

        package_name = ".".join(storage_type.split(".")[:-1])
        storage_name = storage_type.split(".")[-1]

        logger.debug("Initialising storage type: %s%s", package_name + "." if package_name else "", storage_name)

        if package_name:
            logger.debug("Importing storage module %s from package %s", storage_name, package_name)
            # importlib.import_module(storage_name, package_name)
            module = importlib.import_module(package_name)
            self.storage = getattr(module, storage_name)()
        else:
            self.storage = storage_name()

        assert isinstance(self.storage, CustomStorage), "Storage classes should subclass CustomStorage"

    # Required override for custom Storage
    def delete(self, name):
        """
        Delete the specified file from the storage system.
        """
        return self.storage.delete(name)

    # Required override for custom Storage
    def exists(self, name):
        """
        Return True if a file referenced by the given name already exists in the
        storage system, or False if the name is available for a new file.
        """
        return self.storage.exists(name)

    # Required override for custom Storage
    def listdir(self, path):
        """
        List the contents of the specified path. Return a 2-tuple of lists:
        the first item being directories, the second item being files.
        """
        return self.storage.listdir(path)

    # Required override for custom Storage
    def size(self, name):
        """
        Return the total size, in bytes, of the file specified by name.
        """
        return self.storage.size(name)

    # Required override for custom Storage
    def url(self, name):
        """
        Return an absolute URL where the file's contents can be accessed
        directly by a Web browser.
        """
        return self.storage.url(name)

    # Override Storage and delegate to storage system in use
    def open(self, name, mode="rb"):
        """Retrieve the specified file from storage."""
        return self.storage.open(name, mode)

    # Override Storage and delegate to storage system in use
    def save(self, name, content, max_length=None):
        """
        Save new content to the file specified by name. The content should be
        a proper File object or any Python file-like object, ready to be read
        from the beginning.
        """
        return self.storage.save(name, content, max_length)

    # Override Storage and delegate to storage system in use
    def get_valid_name(self, name):
        """
        Return a filename, based on the provided filename, that's suitable for
        use in the target storage system.
        """
        return self.storage.get_valid_name(name)

    # Override Storage and delegate to storage system in use
    def get_alternative_name(self, file_root, file_ext):
        """
        Return an alternative filename, by adding an underscore and a random 7
        character alphanumeric string (before the file extension, if one
        exists) to the filename.
        """
        return self.storage.get_alternative_name(file_root, file_ext)

    # Override Storage and delegate to storage system in use
    def get_available_name(self, name, max_length=None):
        """
        Return a filename that's free on the target storage system and
        available for new content to be written to.
        """
        return self.storage.get_available_name(name, max_length)

    # Override Storage and delegate to storage system in use
    def generate_filename(self, filename):
        """
        Validate the filename by calling get_valid_name() and return a filename
        to be passed to the save() method.
        """
        return self.storage.generate_filename(filename)

    # Override Storage and delegate to storage system in use
    def path(self, name):
        """
        Return a local filesystem path where the file can be retrieved using
        Python's built-in open() function. Storage systems that can't be
        accessed using open() should *not* implement this method.
        """
        raise self.storage.path(name)

    # Override Storage and delegate to storage system in use
    def get_accessed_time(self, name):
        """
        Return the last accessed time (as a datetime) of the file specified by
        name. The datetime will be timezone-aware if USE_TZ=True.
        """
        raise self.storage.get_accessed_time(name)

    # Override Storage and delegate to storage system in use
    def get_created_time(self, name):
        """
        Return the creation time (as a datetime) of the file specified by name.
        The datetime will be timezone-aware if USE_TZ=True.
        """
        raise self.storage.get_created_time(name)

    # Override Storage and delegate to storage system in use
    def get_modified_time(self, name):
        """
        Return the last modified time (as a datetime) of the file specified by
        name. The datetime will be timezone-aware if USE_TZ=True.
        """
        raise self.storage.get_modified_time(name)

    def get_file_contents(self, file_src_path: str):
        return self.storage.get_file_contents(file_src_path)

    def copy_file(self, file_src_path: str, file_dest_path: str = None):
        return self.storage.copy_file(file_src_path, file_dest_path)
