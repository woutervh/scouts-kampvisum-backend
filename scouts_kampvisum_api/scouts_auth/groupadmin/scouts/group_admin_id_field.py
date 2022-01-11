from scouts_auth.inuits.models.fields import OptionalCharField


class GroupAdminIdField(OptionalCharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
