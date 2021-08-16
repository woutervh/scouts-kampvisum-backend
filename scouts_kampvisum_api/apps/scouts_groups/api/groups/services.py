import logging
from django.utils import timezone

from .models import ScoutsAddress
from .models import ScoutsGroupType, ScoutsGroup
from ....groupadmin.api import GroupAdminApi


logger = logging.getLogger(__name__)


class ScoutsGroupService:
    """
    Provides CRUD operations for ScoutsGroup objects.
    """
    
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
                group_type=group_type,
                public_registration=public_registration,
        )
        instance.full_clean()
        instance.save()
        
        for address in addresses:
            address.group = instance
            
            address.full_clean()
            ScoutsAddress.objects.update_or_create()
        
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
        
        instance.full_clean()
        instance.save()
        
        return instance
    
    def import_groupadmin_address(self, address):
        scouts_address = ScoutsAddress()
        
        scouts_address.group_admin_id = address.get('id', '')
        scouts_address.country = address.get('country', '')
        scouts_address.postal_code = address.get('postal_code', '')
        scouts_address.city = address.get('city', '')
        scouts_address.street = address.get('street', '')
        scouts_address.number = address.get('number', '')
        scouts_address.box = address.get('box', '')
        scouts_address.postal_address = address.get('postal_address', False)
        scouts_address.status = address.get('status', '')
        scouts_address.description = address.get('description', '')
        
        location = address.get('location', dict())
        if location:
            scouts_address.latitude = location.get('latitude', ''),
            scouts_address.longitude = location.get('longitude', '')
        
        return scouts_address
    
    def import_groupadmin_group(self, fields):
        group_admin_id = fields.get('group_admin_id', '')
        group_type = ScoutsGroupType.objects.get(type=fields.get(
            'group_type', GroupAdminApi.default_scouts_group_type))
        scouts_group_addresses = list()
        addresses = fields.get('addresses', list())
        for address in addresses:
            scouts_address = self.import_groupadmin_address(address)
            
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
    
    def import_groupadmin_groups(self, groups):
        """
        Imports groups from GroupAdmin, saves them and returns unique objects.
        """
        group_admin_ids = list()
        for group in groups:
            group_admin_ids.append(group.get('group_admin_id'))
            self.import_groupadmin_group(group)
        
        return ScoutsGroup.objects.filter(
            group_admin_id__in=list(set(group_admin_ids))).order_by(
                'group_admin_id')


class ScoutsAddressService:
    
    def address_create(self,
            instance: ScoutsAddress,
            group: ScoutsGroup) -> ScoutsAddress:
        """
        Saves a new ScoutsAddress.
        """
        
        if instance.location:
            instance.location.full_clean()
            instance.location.save()
        
        instance.group = instance
        instance.full_clean()
        instance.save()
        
        return instance
    
    def address_update(self,
            instance: ScoutsAddress,
            group: ScoutsGroup,
            **fields) -> ScoutsAddress:
        """
        Updates an existing ScoutsAddress.
        """
        
        instance.group_admin_id = fields.get('id', instance.group_admin_id)
        instance.country = fields.get('country', '')
        instance.postal_code = fields.get('postal_code', '')
        instance.city = fields.get('city', '')
        instance.street = fields.get('street', '')
        instance.number = fields.get('number', '')
        instance.box = fields.get('box', '')
        instance.postal_address = fields.get('postal_address', False)
        instance.status = fields.get('status', '')
        instance.description = fields.get('description', '')
        instance.group = group
        
        if fields.get('location'):
            pass
        
        instance.full_clean()
        instance.save()
        
        return instance
