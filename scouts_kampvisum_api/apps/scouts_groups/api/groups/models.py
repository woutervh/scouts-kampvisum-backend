from django.db import models
from django.utils import timezone

from ....base.models import BaseModel


class ScoutsGroupType(BaseModel):
    """
    Specifies the type of scouts group (e.g. AKABE, zeescouts, ...).
    """
    
    type = models.CharField(max_length=64)
    
    class Meta:
        abstract = False
        ordering = ['type']
    
    def clean(self):
        pass


class ScoutsLocation(BaseModel):
    """
    Stores a location as a combination of latitude and longitude.
    """
    
    latitude = models.CharField(max_length=64)
    longitude = models.CharField(max_length=64)


class ScoutsAddress(BaseModel):
    """
    Contains an address.
    """
    
    # id
    group_admin_id = models.CharField(max_length=32, unique=True)
    # land
    country = models.CharField(max_length=2)
    # postcode
    postal_code = models.CharField(max_length=32)
    # gemeente
    city = models.CharField(max_length=64)
    # straat
    street = models.CharField(max_length=64)
    # nummer
    number = models.CharField(max_length=12)
    # bus
    box = models.CharField(max_length=12)
    # telefoon
    phone = models.CharField(max_length=64)
    # postadres
    postal_address = models.BooleanField(default = False)
    # status
    status = models.CharField(max_length=12)
    # email
    email = models.CharField(max_length=128)
    # positie
    location = models.ForeignKey(
        ScoutsLocation,
        related_name="location",
        null=True,
        on_delete=models.CASCADE
    ) 
    # omschrijving
    description = models.CharField(max_length=128)


class ScoutsGroup(BaseModel):
    """
    A ScoutsGroup.
    
    Data is loaded with a call to the ScoutsGroupService, using the name
    
    ScoutsAuthGroup fields:
    id = models.AutoField(
        primary_key=True, editable=False)
    name = models.CharField(
        max_length=128)
    location = models.CharField(
        max_length=128)
    uuid = models.UUIDField(
        primary_key=False, default=uuid.uuid4(), editable=False, unique=True)
    """
    
    type = models.ForeignKey(ScoutsGroupType, on_delete=models.CASCADE)
    
    group_admin_id = models.CharField(max_length=32, default='', null=True)
    number = models.CharField(max_length=32, default='', null=True)
    name = models.CharField(max_length=32, default='', null=True)
    addresses = models.ForeignKey(
        ScoutsAddress, 
        related_name="addresses",
        null=True,
        on_delete=models.CASCADE)
    foundation = models.DateTimeField(default=timezone.now, blank=True)
    only_leaders = models.BooleanField(default=False)
    show_members_improved = models.BooleanField(default=False)
    email = models.CharField(max_length=128, default='', null=True)
    website = models.CharField(max_length=128, default='', null=True)
    info = models.CharField(max_length=128, default='', null=True)
    sub_groups = models.ForeignKey(
        "ScoutsGroup",
        related_name="sub_groups",
        null=True,
        on_delete=models.CASCADE
    )
    group_type = models.CharField(max_length=32, default='', null=True)
    public_registration = models.BooleanField(default=False)
    #href
    #sections
    #group_number
    #name
    #addresses
    #onlyLeaders
    #showMembersImproved
    #email
    #website
    #groupType
    #{
    #    'links': [{
    #        'rel': 'self',
    #        'href': 'https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep/X9002G',
    #        'method': 'GET',
    #        'secties': []
    #    }],
    #    'id': 'X9002G',
    #    'groepsnummer': 'X9002G',
    #    'naam': 'Testgroep voor .be-site',
    #    'adressen': [{
    #        'id': '52041acc-fe8a-420a-b4a2-bec286786744',
    #        'land': 'BE',
    #        'postcode': '2140',
    #        'gemeente': ' Borgerhout (Antwerpen)',
    #        'straat': 'Wilrijkstraat',
    #        'nummer': '45',
    #        'bus': '',
    #        'telefoon': '',
    #        'postadres': True,
    #        'status': 'normaal',
    #        'positie': {
    #            'latitude': 51.20923271177719,
    #            'longitude': 4.438153639165718
    #        },
    #        'omschrijving': ''
    #    }],
    #    'opgericht': '2020-09-08T00:00:00.000+02:00',
    #    'enkelLeiding': True,
    #    'ledenVerbeterdTonen': False,
    #    'email': 'info@scoutsengidsenvlaanderen.be',
    #    'website': 'www.scoutsengidsenvlaanderen.be',
    #    'vrijeInfo': '',
    #    'onderliggendeGroepen': [],
    #    'soort': 'Test',
    #    'publiek-inschrijven': False
    #}
    
    def clean(self):
        pass

