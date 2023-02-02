import datetime

from django.db import transaction

from apps.camps.models import Camp
from apps.camps.services import CampYearService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampService:
    year_service = CampYearService()

    @transaction.atomic
    def camp_create(self, request, **fields) -> Camp:
        """
        Saves a Camp object to the DB.
        """

        # Required arguments:
        year = fields.get(
            "year", self.year_service.get_current_camp_year().year)
        name = fields.get("name")
        sections = fields.get("sections")
        # Optional arguments:
        start_date = fields.get("start_date", None)
        end_date = fields.get("end_date", None)

        logger.debug("Creating camp with name '%s' for year %s", name, year)
        camp = Camp()
        camp.year = self.year_service.get_or_create_year(year)
        camp.name = name
        if start_date:
            camp.start_date = start_date
        if end_date:
            camp.end_date = end_date

        camp.full_clean()
        camp.save()

        # logger.debug("Linking %d section(s) to camp '%s'", len(sections), camp.name)
        # section_objects = ScoutsSection.objects.filter(id__in=sections)

        for section in sections:
            camp.sections.add(section)

        camp.save()

        return camp

    @transaction.atomic
    def camp_update(self, request, instance: Camp, **fields) -> Camp:
        """
        Updates an existing Camp object in the DB.
        """
        # logger.debug("Camp update fields: %s", fields)
        # Required arguments:
        instance.name = fields.get("name", instance.name)
        sections = fields.get("sections", instance.sections.all())

        # Optional arguments:
        instance.start_date = fields.get("start_date", instance.start_date)
        instance.end_date = fields.get("end_date", instance.end_date)

        # sections = ScoutsSection.objects.filter(id__in=sections)
        for section in sections:
            instance.sections.add(section)
        for section in instance.sections.all():
            if section not in sections:
                instance.sections.remove(section)

        instance.full_clean()
        instance.save()

        return instance
