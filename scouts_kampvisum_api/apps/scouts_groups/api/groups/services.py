from .models import ScoutsGroup


class ScoutsGroupService():
    
    def group_create(self, *,
                     type,
                     group_admin_id,
                     number,
                     name,
                     addresses,
                     foundation,
                     only_leaders,
                     show_members_improved,
                     email,
                     website,
                     info,
                     sub_groups,
                     group_type,
                     public_registration) -> ScoutsGroup:
        """
        Saves a ScoutsGroup object to the DB.
        """
        
        instance = ScoutsGroup(
            type=type,
            group_admin_id=group_admin_id,
            number=number,
            name=name,
            addresses=addresses,
            foundation=foundation,
            only_leaders=only_leaders,
            show_members_improved=show_members_improved,
            email=email,
            website=website,
            info=info,
            sub_groups=sub_groups,
            group_type=group_type,
            public_registration=public_registration
        )
        
        instance.full_clean()
        instance.save()
        
        return instance