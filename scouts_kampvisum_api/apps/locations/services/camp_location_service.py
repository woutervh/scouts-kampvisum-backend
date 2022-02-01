import logging

from django.http import Http404

from apps.locations.models import CampLocation
from apps.visums.models import LinkedLocationCheck


logger = logging.getLogger(__name__)


class CampLocationService:
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

    def create(self, instance: LinkedLocationCheck, **data) -> CampLocation:
        logger.debug("LOCATION SERVICE CREATE DATA: %s", data)
        latitude = data.get("latitude", None)
        longitude = data.get("longitude", None)
        name = data.get("name", None)
        logger.debug("NAME: %s", name)

        logger.debug("LATITUDE: %s - LONGITUDE: %s", latitude, longitude)

        location = CampLocation()

        location.location_check = instance
        location.name = data.get("name", None)
        location.address = data.get("address", None)
        location.is_main_location = data.get("is_main_location", False)
        location.latitude = latitude
        location.longitude = longitude

        location.full_clean()
        location.save()

        logger.debug("LOCATON: %s", str(location))

        return location

    def update(
        self, instance: LinkedLocationCheck, location: CampLocation, **data
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

    def remove(self, instance: LinkedLocationCheck, location: CampLocation):
        logger.debug(
            "Removing camp location %s from location check %s", location.id, instance.id
        )
        instance.locations.remove(location)
