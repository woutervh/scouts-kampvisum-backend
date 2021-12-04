import logging

from apps.groups.models import ScoutsGroup, ScoutsAddress


logger = logging.getLogger(__name__)


class ScoutsAddressService:
    def address_update_or_create(self, group: ScoutsGroup, fields):
        qs = ScoutsAddress.objects.filter(
            group_admin_uuid=fields.get("group_admin_uuid", "")
        )

        if qs.count() == 1:
            self.address_update(qs[0], group, fields)
        else:
            self.address_create(group, fields)

    def address_create(self, group: ScoutsGroup, fields) -> ScoutsAddress:
        """
        Saves a new ScoutsAddress.
        """

        logger.info("Creating address for group '%s'", group.name)

        instance = ScoutsAddress()

        instance.group_admin_id = fields.get("group_admin_id", "")
        instance.country = fields.get("country", "")
        instance.postal_code = fields.get("postal_code", "")
        instance.city = fields.get("city", "")
        instance.street = fields.get("street", "")
        instance.number = fields.get("number", "")
        instance.letter_box = fields.get("box", "")
        instance.postal_address = fields.get("postal_address", False)
        instance.status = fields.get("status", "")
        instance.latitude = fields.get("latitude", "")
        instance.longitude = fields.get("longitude", "")
        instance.description = fields.get("description", "")
        instance.group = group

        instance.full_clean()
        instance.save()

        return instance

    def address_update(
        self, instance: ScoutsAddress, group: ScoutsGroup, fields
    ) -> ScoutsAddress:
        """
        Updates an existing Address.
        """

        logger.info("Updating address for group '%s'", group.name)

        instance.group_admin_id = fields.get("group_admin_id", instance.group_admin_id)
        instance.country = fields.get("country", instance.country)
        instance.postal_code = fields.get("postal_code", instance.postal_code)
        instance.city = fields.get("city", instance.city)
        instance.street = fields.get("street", instance.street)
        instance.number = fields.get("number", instance.number)
        instance.letter_box = fields.get("box", instance.letter_box)
        instance.postal_address = fields.get("postal_address", instance.postal_address)
        instance.status = fields.get("status", instance.status)
        instance.latitude = fields.get("latitude", instance.latitude)
        instance.longitude = fields.get("longitude", instance.longitude)
        instance.description = fields.get("description", instance.description)
        instance.group = group

        instance.full_clean()
        instance.save()

        return instance
