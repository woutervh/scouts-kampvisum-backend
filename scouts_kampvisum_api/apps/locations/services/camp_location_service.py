import logging
import uuid

from django.core.exceptions import ValidationError
from django.http import Http404

from apps.locations.models import LinkedLocation, CampLocation

from apps.visums.models import LinkedLocationCheck


logger = logging.getLogger(__name__)


class CampLocationService:
    def create_or_update_linked_location(
        self,
        check: LinkedLocationCheck,
        instance: LinkedLocation = None,
        is_camp_location: bool = False,
        **data
    ):
        linked_location_provided = False
        if instance:
            linked_location = LinkedLocation.objects.safe_get(id=instance.id)
            if not linked_location:
                raise ValidationError(
                    "Unable to find LinkedLocation instance with id {}".format(
                        linked_location.id
                    )
                )
            linked_location_provided = True
        else:
            linked_location: LinkedLocation = LinkedLocation.objects.safe_get(
                id=data.get("id", None)
            )

        if linked_location:
            linked_location = self._update_linked_location(
                instance=linked_location, is_camp_location=is_camp_location, **data
            )
        else:
            linked_location = self._create_linked_location(
                is_camp_location=is_camp_location, **data
            )

            check.locations.add(linked_location)

        check.center_latitude = (
            linked_location.center_latitude
            if linked_location.center_latitude
            else check.center_latitude
        )
        check.center_longitude = (
            linked_location.center_longitude
            if linked_location.center_longitude
            else check.center_longitude
        )
        check.zoom = linked_location.zoom if linked_location.zoom else check.zoom

        check.full_clean()
        check.save()

        existing_locations = [
            location.id for location in linked_location.locations.all()
        ]
        logger.debug("LINKED LOCATION CREATE OR UPDATE DATA: %s", data)

        if not linked_location_provided:
            locations = data.get("locations", [])
            posted_locations = [
                uuid.UUID(location.get("id"))
                for location in locations
                if location.get("id", None)
            ]
            for location in existing_locations:
                if not location in posted_locations:
                    CampLocation.objects.get(pk=location).delete()
            for location in locations:
                self.create_or_update(
                    instance=linked_location, check=check, data=location
                )

    def _create_linked_location(
        self, is_camp_location: bool = False, **data
    ) -> LinkedLocation:
        instance = LinkedLocation()

        logger.debug("LINKED LOCATION DATA: %s", data)

        instance.name = data.get("name", None)
        instance.contact_name = data.get("contact_name", None)
        instance.contact_phone = data.get("contact_phone", None)
        instance.contact_email = data.get("contact_email", None)
        instance.is_camp_location = is_camp_location
        instance.center_latitude = data.get("center_latitude", None)
        instance.center_longitude = data.get("center_longitude", None)
        instance.zoom = data.get("zoom", None)

        instance.full_clean()
        instance.save()

        return instance

    def _update_linked_location(
        self, instance: LinkedLocation, is_camp_location: bool = False, **data
    ) -> LinkedLocation:
        instance.name = data.get("name", instance.name)
        instance.contact_name = data.get("contact_name", instance.contact_name)
        instance.contact_phone = data.get("contact_phone", instance.contact_phone)
        instance.contact_email = data.get("contact_email", instance.contact_email)
        instance.is_camp_location = is_camp_location
        instance.center_latitude = data.get("center_latitude", instance.center_latitude)
        instance.center_longitude = data.get(
            "center_longitude", instance.center_longitude
        )
        instance.zoom = data.get("zoom", None)

        instance.full_clean()
        instance.save()

        return instance

    def create_or_update(
        self, instance: LinkedLocation, check: LinkedLocationCheck, data: dict
    ) -> CampLocation:
        logger.debug("CREATE OR UPDATE CAMPLOCATION DATA: %s", data)
        id = data.get("id", None)
        if id:
            location = CampLocation.objects.safe_get(id=data.get("id", None))

            if not location:
                raise ValidationError(
                    "No CampLocation found with id {} for LinkedLocationCheck with id {}".format(
                        id, instance.id
                    )
                )

            return self.update(instance=location, location=instance, **data)
        else:
            return self.create(location=instance, **data)

    def create(self, location: LinkedLocation, **data) -> CampLocation:
        logger.debug("LOCATION SERVICE CREATE DATA: %s", data)

        instance = CampLocation()

        instance.location = location
        instance.name = data.get("name", None)
        instance.address = data.get("address", None)
        instance.is_main_location = data.get("is_main_location", False)
        instance.latitude = data.get("latitude", None)
        instance.longitude = data.get("longitude", None)

        instance.full_clean()
        instance.save()

        # logger.debug("LOCATON: %s", str(location))

        return instance

    def update(
        self, instance: CampLocation, location: LinkedLocation, **data
    ) -> CampLocation:
        logger.debug("LOCATION SERVICE UPDATE DATA: %s", data)

        instance.location = location
        instance.name = data.get("name", instance.name)
        instance.address = data.get("address", instance.address)
        instance.is_main_location = data.get(
            "is_main_location", instance.is_main_location
        )
        instance.latitude = data.get("latitude", instance.latitude)
        instance.longitude = data.get("longitude", instance.longitude)

        instance.full_clean()
        instance.save()

        return instance

    def remove(self, instance: LinkedLocation, location: CampLocation):
        logger.debug(
            "Removing camp location %s from location check %s", location.id, instance.id
        )
        instance.locations.remove(location)
