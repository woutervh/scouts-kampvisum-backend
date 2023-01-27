from django.db.utils import DatabaseError

class DbNotReadyException(DatabaseError):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
