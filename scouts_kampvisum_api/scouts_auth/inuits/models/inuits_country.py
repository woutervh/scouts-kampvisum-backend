from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import OptionalCharField, RequiredCharField
from scouts_auth.inuits.managers import InuitsCountryManager

import logging

logger = logging.getLogger(__name__)


class InuitsCountry(AbstractBaseModel):

    objects = InuitsCountryManager()

    name = RequiredCharField(max_length=64)
    code = OptionalCharField(max_length=2)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED InuitsCountry")
        return self.name
