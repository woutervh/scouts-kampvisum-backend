from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import OptionalCharField, OptionalIntegerField


class InuitsAddress(AbstractNonModel):
    street = OptionalCharField(max_length=100)
    number = OptionalCharField(max_length=5)
    letter_box = OptionalCharField(max_length=5)
    postal_code = OptionalCharField()
    city = OptionalCharField(max_length=40)
    # country = models.ForeignKey(InuitsCountry, on_delete=models.CASCADE, null=True, related_name="address")

    class Meta:
        abstract = True

    def address_details_to_str(self):
        return (
            "street({}), number({}), letter_box({}), postal_code({}), city({})".format(
                self.street, self.number, self.letter_box, self.postal_code, self.city
            )
        )

    def equals_address(self, updated_address) -> bool:
        if updated_address is None:
            return False

        if not type(updated_address).__class__.__name__ == self.__class__.__name__:
            return False

        return (
            self.street == updated_address.street
            and self.number == updated_address.number
            and self.letter_box == updated_address.letter_box
            and self.postal_code == updated_address.postal_code
            and self.city == updated_address.city
        )
