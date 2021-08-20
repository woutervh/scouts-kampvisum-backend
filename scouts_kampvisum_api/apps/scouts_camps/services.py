import uuid, logging
from .models import ScoutsCamp
from apps.scouts_groups.api.sections.models import ScoutsSection


logger = logging.getLogger(__name__)


class ScoutsCampService():
    
    def camp_create(self, *args, **fields) -> ScoutsCamp:
        """
        Saves a ScoutsCamp object to the DB.
        """

        #Required arguments:
        name = fields.get('name')
        sections = fields.get('sections')
        # Optional arguments:
        start_date = fields.get('start_date', None)
        end_date = fields.get('end_date', None)
        
        camp = ScoutsCamp()
        camp.name = name
        if start_date:
            camp.start_date = start_date
        if end_date:
            camp.end_date = end_date
        
        camp.full_clean()
        camp.save()

        sections = ScoutsSection.objects.filter(uuid__in=sections)
        for section in sections:
            camp.sections.add(section)
        camp.save()
        
        return camp
    
    def camp_update(self, *, instance: ScoutsCamp, **fields) -> ScoutsCamp:
        """
        Updates an existing ScoutsCamp object in the DB.
        """
        
        instance.name = fields.get('name', instance.name)
        instance.start_date = fields.get('start_date', instance.start_date)
        instance.end_date = fields.get('end_date', instance.end_date)
        
        instance.full_clean()
        instance.save()
        
        return instance

