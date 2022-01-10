from apps.people.models import ContactPerson
from apps.people.serializers import PersonSerializer


class ContactPersonSerializer(PersonSerializer):
    class Meta:
        model = ContactPerson
        fields = "__all__"
