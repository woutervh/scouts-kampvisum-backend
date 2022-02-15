import logging
import uuid

from django.http import Http404

from apps.locations.models import LinkedLocation, CampLocation

from apps.visums.models import LinkedLocationCheck


logger = logging.getLogger(__name__)


class CampLocationService:
    def create_or_update_linked_location(
        self, check: LinkedLocationCheck, is_camp_location: bool = False, **data
    ):
        logger.debug("CAMP LOCATION SERVICE DATA: %s", data)
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

            check.value.add(linked_location)

        check.center_latitude = linked_location.center_latitude
        check.center_longitude = linked_location.center_longitude
        check.zoom = linked_location.zoom

        check.full_clean()
        check.save()

        existing_locations = [
            location.id for location in linked_location.locations.all()
        ]
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
            self.create_or_update(instance=linked_location, data=location)

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
        self, instance: LinkedLocationCheck, data: dict
    ) -> CampLocation:
        id = data.get("id", None)
        if id:
            try:
                location = CampLocation.objects.get(pk=id)
            except:
                raise Http404(
                    "No CampLocation found with id {} for LinkedLocationCheck with id {}".format(
                        id, instance.id
                    )
                )

            return self.update(instance, location, **data)
        else:
            return self.create(instance, **data)

    def create(self, instance: LinkedLocation, **data) -> CampLocation:
        logger.debug("LOCATION SERVICE CREATE DATA: %s", data)

        latitude = data.get("latitude", None)
        longitude = data.get("longitude", None)
        name = data.get("name", None)

        location = CampLocation()

        location.location_check = instance
        location.name = name
        location.address = data.get("address", None)
        location.is_main_location = data.get("is_main_location", False)
        location.latitude = latitude
        location.longitude = longitude

        location.full_clean()
        location.save()

        logger.debug("LOCATON: %s", str(location))

        return location

    def update(
        self, instance: LinkedLocation, location: CampLocation, **data
    ) -> CampLocation:
        logger.debug("LOCATION SERVICE UPDATE DATA: %s", data)

        location.location_check = instance
        location.name = data.get("name", location.name)
        location.address = data.get("address", location.address)
        location.is_main_location = data.get(
            "is_main_location", location.is_main_location
        )
        location.latitude = data.get("latitude", location.latitude)
        location.longitude = data.get("longitude", location.longitude)

        location.full_clean()
        location.save()

        return location

    def remove(self, instance: LinkedLocation, location: CampLocation):
        logger.debug(
            "Removing camp location %s from location check %s", location.id, instance.id
        )
        instance.locations.remove(location)
