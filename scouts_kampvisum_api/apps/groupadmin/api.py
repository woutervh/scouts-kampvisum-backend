import requests, logging
from django.conf import settings

logger = logging.getLogger(__name__)
base_endpoint = settings.GROUP_ADMIN_BASE_ENDPOINT
active_user = settings.AUTH_USER_MODEL

class GroupAdminApi:
    """
    Constructs endpoints for various GroupAdmin API calls.
    """
    
    @staticmethod
    def get_request(endpoint):
        return requests.get("{0}".format(endpoint),
            headers={"Authorization": "Bearer {0}".format(
                active_user.access_token)},
        )
    
    @staticmethod
    def get_groups_endpoint():
        """
        Return all groups for which the user has rights.
        
        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groepen-get
        """
        
        return base_endpoint + '/groep'

