from scouts_auth.inuits.models import AbstractNonModel


class AbstractScoutsMedicalFlashCard(AbstractNonModel):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        pass
