import logging

from django.http import Http404

from apps.locations.models import CampLocation
from apps.visums.models import LinkedLocationCheck


logger = logging.getLogger(__name__)


class CampLocationService:
    def create_or_update(self, instance: LinkedLocationCheck, **data):
        logger.debug("LOCATION SERVICE DATA: %s", data)
        id = data.get("id", None)

        location_data = dict()
        keys = data.keys()
        for key in keys:
            element = data.get(key)
            location_data = element
            logger.debug("ELEMENT: %s", element)
            element_keys = element.keys()
            for element_key in element_keys:
                logger.debug("ITEM: %s", element.get(element_key))
        logger.debug("TEST: %s", data.get("name"))

        if id:
            location = CampLocation.objects.get(pk=id)

            if not location:
                raise Http404(
                    "No CampLocation found with id {} for LinkedLocationCheck with id {}".format(
                        id, instance.id
                    )
                )

            return self.update(instance, location, **data)
        else:
            return self.create(instance, **location_data)

    def create(self, instance: LinkedLocationCheck, **data):
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
        location.zoom = data.get("zoom", None)

        location.full_clean()
        location.save()

        logger.debug("LOCATON: %s", str(location))

        return location

    def update(self, instance: LinkedLocationCheck, location: CampLocation, **data):
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
