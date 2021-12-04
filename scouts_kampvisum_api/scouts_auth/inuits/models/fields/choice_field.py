from django.db.models import TextChoices


class ChoiceField:
    def __init__(self, model: TextChoices):
        model.fields

    def to_internal_value(self, data):
        if isinstance(data, list):
            return []
        else:
            return ""

    def to_representation(self, obj):
        if isinstance(obj, list):
            return []
        else:
            return ""
