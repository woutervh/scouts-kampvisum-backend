from scouts_auth.inuits.models.fields import RequiredCharField, OptionalCharField


class GroupAdminIdField(RequiredCharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 48
        super().__init__(*args, **kwargs)


class OptionalGroupAdminIdField(OptionalCharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 48
        super().__init__(*args, **kwargs)
