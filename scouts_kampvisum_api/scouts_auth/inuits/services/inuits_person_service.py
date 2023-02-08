from datetime import datetime

from django.db import transaction

from scouts_auth.inuits.models import (
    Gender,
    InuitsPersonalDetails,
    InuitsAddress,
    InuitsCountry,
)


class InuitsPersonService:
    @transaction.atomic
    def inuits_personal_details_create(
        self,
        first_name: str = "",
        last_name: str = "",
        phone_number: str = "",
        cell_number: str = "",
        email: str = "",
        birth_date: datetime.date = None,
        gender: Gender = Gender.UNKNOWN,
    ) -> InuitsPersonalDetails:
        personal_details = InuitsPersonalDetails(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            cell_number=cell_number,
            email=email,
            birth_date=birth_date,
            gender=gender,
        )

        personal_details.full_clean()
        personal_details.save()

        return personal_details

    @transaction.atomic
    def inuits_address_details_create(
        self,
        street: str = "",
        number: str = "",
        letter_box: str = "",
        postal_code: int = None,
        city: str = "",
        country: InuitsCountry = None,
    ) -> InuitsAddress:
        address_details = InuitsAddress(
            street=street,
            number=number,
            letter_box=letter_box,
            postal_code=postal_code,
            city=city,
            country=country,
        )
        address_details.full_clean()
        address_details.save()

        return address_details

    def inuits_personal_details_update(
        self, *, personal_details: InuitsPersonalDetails, **fields
    ) -> InuitsPersonalDetails:
        personal_details.first_name = fields.get(
            "first_name", personal_details.first_name
        )
        personal_details.last_name = fields.get(
            "last_name", personal_details.last_name)
        personal_details.phone_number = fields.get(
            "phone_number", personal_details.phone_number
        )
        personal_details.cell_number = fields.get(
            "cell_number", personal_details.cell_number
        )
        personal_details.birth_date = fields.get(
            "birth_date", personal_details.birth_date
        )
        personal_details.gender = fields.get("gender", personal_details.gender)

        personal_details.full_clean()
        personal_details.save()

        return personal_details

    def inuits_address_details_update(
        self, *, address_details: InuitsAddress, **fields
    ) -> InuitsAddress:
        address_details.street = fields.get("street", address_details.street)
        address_details.number = fields.get("number", address_details.number)
        address_details.letter_box = fields.get(
            "letter_box", address_details.letter_box
        )
        address_details.postal_code = fields.get(
            "postal_code", address_details.postal_code
        )
        address_details.city = fields.get("city", address_details.city)
        address_details.country = fields.get(
            "country", address_details.country)
        address_details.comment = fields.get(
            "comment", address_details.comment)

        address_details.full_clean()
        address_details.save()

        return address_details
