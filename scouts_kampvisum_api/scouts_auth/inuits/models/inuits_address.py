from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import OptionalCharField, OptionalIntegerField


class InuitsAddress(AbstractNonModel):
    street = OptionalCharField(max_length=100)
    number = OptionalCharField(max_length=5)
    letter_box = OptionalCharField(max_length=5)
    postal_code = OptionalIntegerField()
    city = OptionalCharField(max_length=40)
    # country = models.ForeignKey(InuitsCountry, on_delete=models.CASCADE, null=True, related_name="address")

    class Meta:
        abstract = True

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.street = kwargs.get("street", "")
    #     self.number = kwargs.get("number", "")
    #     self.letter_box = kwargs.get("letter_box", "")
    #     self.postal_code = kwargs.get("postal_code", "")
    #     self.city = kwargs.get("city", "")

    def address_details_to_str(self):
        return "street({}), number({}), letter_box({}), postal_code({}), city({})".format(
            self.street, self.number, self.letter_box, self.postal_code, self.city
        )
