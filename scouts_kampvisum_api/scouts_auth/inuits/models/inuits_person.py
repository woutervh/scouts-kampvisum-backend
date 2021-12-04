from scouts_auth.inuits.models import (
    AuditedBaseModel,
    InuitsPersonalDetails,
    InuitsAddress,
)


class InuitsPerson(InuitsPersonalDetails, InuitsAddress, AuditedBaseModel):

    # personal_details = models.OneToOneField(InuitsPersonalDetails, on_delete=models.CASCADE)
    # address_details = models.ForeignKey(InuitsAddress, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    # @property
    # def first_name(self) -> str:
    #     return self.personal_details.first_name

    # @first_name.setter
    # def first_name(self, first_name: str):
    #     self.personal_details.first_name = first_name

    # @property
    # def last_name(self) -> str:
    #     return self.personal_details.last_name

    # @last_name.setter
    # def last_name(self, last_name: str):
    #     self.personal_details.last_name = last_name

    # @property
    # def phone_number(self) -> str:
    #     return self.personal_details.phone_number

    # @phone_number.setter
    # def phone_number(self, phone_number: str):
    #     self.personal_details.phone_number = phone_number

    # @property
    # def cell_number(self) -> str:
    #     return self.personal_details.cell_number

    # @cell_number.setter
    # def cell_number(self, cell_number: str):
    #     self.personal_details.cell_number = cell_number

    # @property
    # def email(self) -> str:
    #     return self.personal_details.email

    # @email.setter
    # def email(self, email: str):
    #     self.personal_details.email = email

    # @property
    # def birth_date(self) -> date:
    #     return self.personal_details.birth_date

    # @birth_date.setter
    # def birth_date(self, birth_date: date):
    #     self.personal_details.birth_date = birth_date

    # @property
    # def gender(self) -> Gender:
    #     return self.personal_details.gender

    # @gender.setter
    # def gender(self, gender: Gender):
    #     self.personal_details.gender = gender

    # @property
    # def street(self) -> str:
    #     return self.address_details.street

    # @street.setter
    # def street(self, street: str):
    #     self.address_details.street = street

    # @property
    # def number(self) -> str:
    #     return self.address_details.number

    # @street.setter
    # def number(self, number: str):
    #     self.address_details.number = number

    # @property
    # def letter_box(self) -> str:
    #     return self.address_details.letter_box

    # @letter_box.setter
    # def letter_box(self, letter_box: str):
    #     self.address_details.letter_box = letter_box

    # @property
    # def postal_code(self) -> str:
    #     return self.address_details.postal_code

    # @postal_code.setter
    # def postal_code(self, postal_code: str):
    #     self.address_details.postal_code = postal_code

    # @property
    # def city(self) -> str:
    #     return self.address_details.city

    # @city.setter
    # def city(self, city: str):
    #     self.address_details.city = city

    # @property
    # def country(self) -> InuitsCountry:
    #     return self.address_details.country

    # @country.setter
    # def country(self, country: InuitsCountry):
    #     self.address_details.country = country

    # @property
    # def address(self) -> InuitsAddress:
    #     return InuitsAddress(
    #         street=self.street,
    #         number=self.number,
    #         letter_box=self.letter_box,
    #         postal_code=self.postal_code,
    #         city=self.city,
    #         country=self.country,
    #     )
