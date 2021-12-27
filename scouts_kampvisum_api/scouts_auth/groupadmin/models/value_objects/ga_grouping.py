from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import OptionalCharField, OptionalIntegerField


class AbstractScoutsGrouping(AbstractNonModel):

    name = OptionalCharField()
    index = OptionalIntegerField()

    class Meta:
        abstract = True

    def __init__(self, name: str = "", index: int = -1):
        self.name = name
        self.index = index

        # super().__init__([], {})

    def __str__(self):
        return "name({}), index({})".format(self.name, self.index)
