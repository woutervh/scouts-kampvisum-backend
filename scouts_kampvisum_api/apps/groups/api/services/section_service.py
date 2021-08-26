import logging, warnings
from django.db.models import Q
from django.shortcuts import get_object_or_404

from ..models import (
    SectionName,
    Group,
    Section,
)
from ..services import SectionNameService


logger = logging.getLogger(__name__)


class SectionService:

    section_name_service = SectionNameService()
    
    def section_create_or_update(self,
        group=None, name=None, hidden=False, **fields) -> Section:
        """
        Creates or updates a Section instance.
        """
        logger.debug(
            "GROUP, NAME, HIDDEN: %s %s %s", group, name, hidden)
        if not isinstance(group, Group):
            from ..services import GroupService
            group = GroupService().get_group(group)

        name_instance = None
        if not isinstance(name, SectionName):
            name_instance = self.section_name_service.name_get(name=name)

        if name_instance is None:
            qs = Section.objects.filter(group=group, name__name=name)
        else:
            qs = Section.objects.filter(group=group, name=name)
        count = qs.count()

        if count > 0:
            warnings.warn("Attempted to create or update multiple objects")
            return None


        if count == 0:
            logger.debug("Creating Section with name '%s'", name)
            return self._section_create(group, name, hidden, **fields)
        if count == 1:
            instance = qs[0]
            logger.debug(
                "Updating Section with name '%s'", instance.name.name)
            return self._section_update(
                instance, group, name, hidden, **fields)


    def _section_create(self,
        group=None, name=None, hidden=False, **fields) -> Section:
        if name is None or not isinstance(name, SectionName):
            name = self.section_name_service.name_create(name=name)
        instance = Section()

        instance.group = group
        instance.name = name
        instance.hidden = hidden

        instance.full_clean()
        instance.save()

        return instance
    
    def _section_update(self,
        instance: Section,
        group: Group = None,
        name: SectionName = None,
        hidden=False, **fields) -> Section:
        """
        Updates an existing Section instance.
        """
        logger.debug(
            "Updating Section with name '%s'", instance.name.name)

        instance.group = group
        instance.name = name
        instance.hidden = hidden

        instance.full_clean()
        instance.save()

        return instance
    
    def section_read(self, *args, **fields) -> Section:
        """
        Retrieves a Section by uuid or SectionName.

        If uuid or name are lists, then lists will be returned.
        If uuid is None, then the group argument must be presented.
        """
        group = fields.get('group', None)
        uuid = fields.get('uuid', None)
        name = fields.get('name', None)

        logger.debug("SECTION FIELDS: %s", fields)

        if uuid is None and name is None:
            return Section.objects.all()
        
        if uuid is not None and not isinstance(uuid, dict):
            if isinstance(uuid, list):
                return list(Section.objects.filter(
                    uuid__in=uuid).values_list())

            if isinstance(uuid, uuid.UUID):
                return get_object_or_404(Section, uuid=uuid)

        if name is not None and not isinstance(name, dict):
            if isinstance(name, list):
                return list(Section.objects.filter(
                    group=group,
                    name__name__in=name).values_list())
            
            if isinstance(name, str):
                return list(Section.objects.filter(
                    group=group, name__name=name))
        
        logger.debug('No Section instances found with the given args')
        
        return None

