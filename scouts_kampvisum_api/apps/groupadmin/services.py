import requests, logging
from django.conf import settings

from .api import GroupAdminApi as api
from ..scouts_groups.api.groups.models import ScoutsGroup

logger = logging.getLogger(__name__)

class GroupAdminService:
    
    def get_group(
            self, href: str) -> ScoutsGroup:
        response = requests.get(href)
        
        response.raise_for_status()
        json = response.json()
        
        logger.info("GROUP")
        logger.info(json)
        
        addresses = json.get('adressen', [])
        
        return None
    
    def get_groups(self, groups):
        response = api.get_request(api.get_groups_endpoint())
        
        json = response.json()
        
        logger.info('GROUPS: %s', json)
        
        return None
