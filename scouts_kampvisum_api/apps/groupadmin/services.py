import requests, logging
from django.conf import settings

from scouts_auth.models import User as ScoutsAuthUser
from .api import GroupAdminApi as api
from apps.groups.api.models import Group
from apps.groups.api.serializers import GroupSerializer

logger = logging.getLogger(__name__)

class GroupAdminService:
    
    def get_group(
            self, href: str) -> Group:
        response = requests.get(href)
        
        response.raise_for_status()
        json = response.json()
        
        return json
    
    def get_groups(self, active_user:ScoutsAuthUser):
        active_user.fetch_detailed_group_info()
        group_links = active_user.partial_scouts_groups
        groups = []
        
        for href in group_links:
            groups.append(self.get_group(href))
        
        return groups

