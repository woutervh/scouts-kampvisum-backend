from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import OptionalCharField


class AbstractScoutsValue(AbstractNonModel):

    key = OptionalCharField()
    value = OptionalCharField()

    class Meta:
        abstract = True

    def __init__(self, key: str = "", value: str = ""):
        self.key = key
        self.value = value

        # super().__init__([], {})

    def __str__(self):
        return "[key({}), value({})]".format(self.key, self.value)
