from rest_framework import serializers

class OptionalDateField(serializers.DateField):
    """
    Initializes a serializers.DateField that is optional.

    This is equivalent to setting a serializer.DateField as such:
    some_optional_date_field = serializers.DateField(
        required=False, default=None, allow_null=True
    )
    """

    def __init__(self, *args, **kwargs):
        kwargs['required'] = False
        kwargs['default'] = None
        # This fixes the validation error when the key for a date field
        # is set in JSON with a value of null.
        kwargs['allow_null'] = True
        super().__init__(*args, **kwargs)

