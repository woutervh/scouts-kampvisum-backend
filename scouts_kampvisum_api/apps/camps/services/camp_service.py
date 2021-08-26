import uuid
import logging
from ..models import Camp
from apps.groups.api.models import Section


logger = logging.getLogger(__name__)


class CampService():

    def camp_create(self, *args, **fields) -> Camp:
        """
        Saves a Camp object to the DB.
        """

        # Required arguments:
        year = fields.get('year')
        name = fields.get('name')
        sections = fields.get('sections')
        # Optional arguments:
        start_date = fields.get('start_date', None)
        end_date = fields.get('end_date', None)

        camp = Camp()
        camp.year = year
        camp.name = name
        if start_date:
            camp.start_date = start_date
        if end_date:
            camp.end_date = end_date

        camp.full_clean()
        camp.save()

        sections = Section.objects.filter(uuid__in=sections)
        for section in sections:
            camp.sections.add(section)
        camp.save()

        return camp

    def camp_update(self, *, instance: Camp, **fields) -> Camp:
        """
        Updates an existing Camp object in the DB.
        """

        # Required arguments:
        instance.name = fields.get('name', instance.name)
        sections = fields.get('sections')

        # Optional arguments:
        instance.start_date = fields.get('start_date', instance.start_date)
        instance.end_date = fields.get('end_date', instance.end_date)

        sections = Section.objects.filter(uuid__in=sections)
        instance.sections.clear()
        for section in sections:
            instance.sections.add(section)

        instance.full_clean()
        instance.save()

        return instance
