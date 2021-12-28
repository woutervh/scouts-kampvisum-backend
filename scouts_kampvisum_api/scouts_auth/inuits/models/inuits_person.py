from scouts_auth.inuits.models import (
    AuditedBaseModel,
    InuitsPersonalDetails,
    InuitsAddress,
)


class InuitsPerson(InuitsPersonalDetails, InuitsAddress, AuditedBaseModel):
    class Meta:
        abstract = True

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def person_to_str(self):
        return self.personal_details_to_str() + ", " + self.address_details_to_str()
