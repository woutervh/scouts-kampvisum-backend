import logging, uuid
from django.utils import timezone

from scouts_auth.models import User as ScoutsAuthUser
from apps.groupadmin.api import GroupAdminApi
from apps.groupadmin.services import GroupAdminService
from apps.groupadmin.serializers import GroupAdminGroupSerializer

from ..models import ScoutsGroupType, ScoutsGroup
from ..services import (
    ScoutsAddressService,
    ScoutsDefaultSectionNameService,
    ScoutsSectionService,
)


logger = logging.getLogger(__name__)


class ScoutsGroupService:
    """
    Provides CRUD operations for ScoutsGroup objects.
    """

    def get_group(self, uuid_string):
        """
        Convenience method to allow REST calls with uuid strings
        """
        uuid = uuid.uuid(uuid_string)

        return ScoutsGroup.objects.get(uuid=uuid)
    
    def group_create(self, 
                     group_admin_id,
                     number,
                     name,
                     foundation,
                     only_leaders,
                     show_members_improved,
                     email,
                     website,
                     info,
                     group_type,
                     public_registration,
                     addresses,
                     sub_groups,) -> ScoutsGroup:
        """
        Saves a ScoutsGroup object to the DB.
        """
        
        logger.info(
            "Saving ScoutsGroup with name: '%s' and id: '%s'",
            name, group_admin_id)
        
        instance = ScoutsGroup(
                group_admin_id=group_admin_id,
                number=number,
                name=name,
                foundation=foundation,
                only_leaders=only_leaders,
                show_members_improved=show_members_improved,
                email=email,
                website=website,
                info=info,
                #sub_groups=sub_groups,
                type=group_type,
                public_registration=public_registration,
        )
        instance.full_clean()
        instance.save()
        
        for address in addresses:
            ScoutsAddressService().address_update_or_create(instance, address)
        
        return instance
    
    def group_update(self,
                     instance: ScoutsGroup,
                     addresses,
                     sub_groups,
                     fields,) -> ScoutsGroup:
        """
        Updates a ScoutsGroup object with current values.
        """
        
        logger.info(
            "Updating ScoutsGroup with name: '%s' and id: '%s'",
            instance.name, instance.group_admin_id)
        
        instance.group_admin_id = fields.get(
            'group_admin_id', instance.group_admin_id)
        instance.number = fields.get('number', instance.number)
        instance.name = fields.get('name', instance.name)
        instance.foundation = fields.get('foundation', instance.foundation)
        instance.only_leaders = fields.get(
            'only_leaders', instance.only_leaders)
        instance.show_members_improved = fields.get(
            'show_members_improved', instance.show_members_improved)
        instance.email = fields.get('email', instance.email)
        instance.website = fields.get('website', instance.website)
        instance.info = fields.get('info', instance.info)
        instance.type = ScoutsGroupType.objects.get(type=fields.get('type'))
        
        instance.full_clean()
        instance.save()
        
        for address in addresses:
            ScoutsAddressService().address_update_or_create(instance, address)
        
        return instance
    
    def flatten_groupadmin_address(self, fields):
        """
        Flattens latitude and longitude into the address dictionary.
        """
        
        location = fields.get('location', None)
        if location:
            fields['latitude'] = location.get('latitude', '')
            fields['longitude'] = location.get('longitude', '')
            fields.pop('location')
        
        return fields
    
    def import_groupadmin_group(self, fields):
        """
        Parses GroupAdmin group data and saves it as a ScoutsGroup object.
        """
        
        group_admin_id = fields.get('group_admin_id', '')
        group_type = ScoutsGroupType.objects.get(type=fields.get(
            'type', GroupAdminApi.default_scouts_group_type))
        
        scouts_group_addresses = list()
        addresses = fields.get('addresses', list())
        for address in addresses:
            scouts_address = self.flatten_groupadmin_address(
                address)
            
            scouts_group_addresses.append(scouts_address)
        
        scouts_group_sub_groups = list()
        sub_groups = fields.get('sub_groups', list())
        for sub_group in sub_groups:
            scouts_sub_group = self.import_groupadmin_group(sub_group)
            
            scouts_group_sub_groups.append(scouts_sub_group)
        
        qs = ScoutsGroup.objects.filter(group_admin_id=group_admin_id)
        
        if qs.count() == 1:
            instance = self.group_update(
                qs[0],
                scouts_group_addresses,
                scouts_group_sub_groups,
                fields,
            )
        else:
            # Assume that the database was clean at this point and no other
            # objects with the same group_admin_id exist.
            instance = self.group_create(
                group_admin_id,
                fields.get('number', ''),
                fields.get('name', ''),
                fields.get('foundation', timezone.now()),
                fields.get('only_leaders', False),
                fields.get('show_members_improved', False),
                fields.get('email', ''),
                fields.get('website', ''),
                fields.get('info', ''),
                group_type,
                fields.get('public_registration', False),
                scouts_group_addresses,
                scouts_group_sub_groups
            )
        
        return instance
    
    def import_groupadmin_groups(self, user:ScoutsAuthUser):
        """
        Imports groups from GroupAdmin, saves them and returns unique objects.
        """
        
        group_admin_ids = list()
        groups = GroupAdminService().get_groups(user)
        serializer = GroupAdminGroupSerializer(groups, many=True)
        
        for group in serializer.data:
            group_admin_ids.append(group.get('group_admin_id'))
            self.import_groupadmin_group(group)
        
        return ScoutsGroup.objects.filter(
            group_admin_id__in=list(set(group_admin_ids))).order_by(
                'group_admin_id')
    
    def link_default_sections(self):
        """
        Links default sections to a group.
        """

        groups = ScoutsGroup.objects.all()
        service = ScoutsDefaultSectionNameService()
        section_service = ScoutsSectionService()
        creation_count = 0

        for group in groups:
            logger.debug('GROUP: %s (%s)',
                group, group.name)

            sections = group.sections.all()

            logger.debug('SECTIONS: %s (%s)',
                sections, sections.count())
            if sections.count() == 0:
                names = service.load_for_type(group.type)

                logger.debug('NAMES: %s (%s)',
                    names, len(names))

                for name in names:
                    logger.debug('NAME: %s', name)
                    section = section_service.create(group, name.name, False)
                    creation_count += 1
        
        return creation_count

