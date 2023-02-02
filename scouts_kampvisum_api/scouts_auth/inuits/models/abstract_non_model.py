from django.db import models


class AbstractNonModel(models.Model):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
