from scouts_auth.inuits.models import AbstractNonModel, Gender, GenderHelper
from scouts_auth.inuits.models.fields import (
    OptionalCharField,
    DefaultCharField,
    RequiredCharField,
    OptionalEmailField,
    OptionalDateField,
)


class InuitsPersonalDetails(AbstractNonModel):
    first_name = RequiredCharField(max_length=15)
    last_name = RequiredCharField(max_length=25)
    phone_number = OptionalCharField(max_length=24)
    cell_number = OptionalCharField(max_length=24)
    email = OptionalEmailField()
    birth_date = OptionalDateField()
    gender = DefaultCharField(choices=Gender.choices, default=Gender.UNKNOWN, max_length=1)

    class Meta:
        abstract = True

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.first_name = kwargs.get("first_name", "")
    #     self.last_name = kwargs.get("last_name", "")
    #     self.phone_number = kwargs.get("phone_number", "")
    #     self.cell_number = kwargs.get("cell_number", "")
    #     self.email = kwargs.get("email", "")
    #     self.birth_date = kwargs.get("birth_date", None)
    #     self.gender = GenderHelper.parse_gender(kwargs.get("gender", None))

    def personal_details_to_str(self):
        return "first_name({}), last_name({}), phone_number({}), cell_number({}), email({}), birth_date({}), gender({})".format(
            self.first_name,
            self.last_name,
            self.phone_number,
            self.cell_number,
            self.email,
            self.birth_date,
            self.gender,
        )
