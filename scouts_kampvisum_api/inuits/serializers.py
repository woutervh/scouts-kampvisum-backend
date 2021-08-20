from rest_framework import serializers

class OptionalDateField(serializers.DateField):
    """
    Initializes a serializers.DateField that is optional.

    This is equivalent to setting a serializer.DateField as such:
    some_optional_date_field = serializers.DateField(
        required=False
    )
    """

    def __init__(self, *args, **kwargs):
        kwargs['required'] = False
        super().__init__(*args, **kwargs)

