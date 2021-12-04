import logging

from scouts_auth.inuits.files import StorageService


logger = logging.getLogger(__name__)


class EmailAttachment:
    file_path: str = None
    file_service: StorageService = None

    def __init__(self, file_path: str, file_service: StorageService = None):
        self.file_path = file_path
        self.file_service = file_service

    def get_file_and_contents(self, file_dest_path: str = None):
        """Returns a tuple of file name and file contents."""
        if self.file_service:
            return (self.file_path, self.file_service.get_file_contents(self.file_path))

        with open(self.file_path, "rb") as f:
            return (self.file_path, f.read())


class Email:

    subject: str = ""
    body: str = ""
    from_email: str = None
    to: list = None
    cc: list = None
    bcc: list = None
    reply_to: str = None
    attachment_paths: list = None
    attachments: list = None
    template_id: str = None

    # https://stackoverflow.com/questions/4535667/python-list-should-be-empty-on-class-instance-initialisation-but-its-not-why
    def __init__(
        self,
        subject: str = "",
        body: str = "",
        from_email: str = None,
        to: list = None,
        cc: list = None,
        bcc: list = None,
        reply_to: str = None,
        attachment_paths: list = None,
        attachments: list = None,
        template_id=None,
    ):
        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.to = self._parse_arguments(to)
        self.cc = self._parse_arguments(cc)
        self.bcc = self._parse_arguments(bcc)
        self.reply_to = reply_to if reply_to else from_email
        self.attachment_paths = self._parse_arguments(attachment_paths)
        self.attachments = self._parse_arguments(attachments)
        self.template_id = template_id

    def _parse_arguments(self, arguments) -> list:
        if not arguments:
            return []
        if isinstance(arguments, list):
            return arguments
        return [arguments]

    def add_attachment_path(self, attachment_path: str):
        self.attachment_paths.append(attachment_path)

    def add_attachment(self, attachment: EmailAttachment):
        self.attachments.append(attachment)

    def has_attachments(self) -> bool:
        return len(self.attachments) > 0
