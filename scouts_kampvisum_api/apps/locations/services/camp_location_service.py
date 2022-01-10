import logging

from django.http import Http404

from apps.locations.models import CampLocation
from apps.visums.models import LinkedLocationCheck


logger = logging.getLogger(__name__)


class CampLocationService:
    def create_or_update(self, instance: LinkedLocationCheck, **data):
        id = data.get("id", None)

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
            return self.create(instance, **data)

    def create(self, instance: LinkedLocationCheck, **data):
        location = CampLocation()

        location.location_check = instance
        location.name = data.get("name", None)
        location.address = data.get("address", None)
        location.is_main_location = data.get("is_main_location", False)
        location.latitude = data.get("latitude", None)
        location.longitude = data.get("longitude", None)

        location.full_clean()
        location.save()

        return location

    def create(self, instance: LinkedLocationCheck, location: CampLocation, **data):
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
