from scouts_auth.groupadmin.models import AbstractScoutsMedicalFlashCard
from scouts_auth.inuits.serializers import NonModelSerializer


class AbstractScoutsMedicalFlashCardSerializer(NonModelSerializer):
    class Meta:
        model = AbstractScoutsMedicalFlashCard
        abstract = True
