from rest_framework import serializers


class OptionalCharField(serializers.CharField):
    """
    Initializes a serializers.CharField that is optional.

    This is equivalent to setting a serializer.CharField as such:
    some_optional_char_field = serializers.CharField(
        default=empty, required=False, allow_blank=True, allow_null=True
    )
    """

    def __init__(self, *args, **kwargs):
        kwargs['default'] = serializers.empty
        kwargs['required'] = False
        kwargs['allow_blank'] = True
        # This fixes the validation error when the key for a char field
        # is set in JSON with a value of null.
        kwargs['allow_null'] = True
        super().__init__(*args, **kwargs)


class OptionalIntegerField(serializers.IntegerField):
    """
    Initializes a serializers.IntegerField that is optional.

    This is equivalent to setting a serializer.IntegerField as such:
    some_optional_integer_field = serializers.IntegerField(
        default=empty, required=False, allow_null=True
    )
    """

    def __init__(self, *args, **kwargs):
        kwargs['default'] = serializers.empty
        kwargs['required'] = False
        # This fixes the validation error when the key for an integer field
        # is set in JSON with a value of null.
        kwargs['allow_null'] = True
        super().__init__(*args, **kwargs)


class OptionalChoiceField(serializers.ChoiceField):
    """
    Initializes a serializers.ChoiceField that is optional.

    This is equivalent to setting a serializer.ChoiceField as such:
    some_optional_choice_field = serializers.ChoiceField(
        default=empty, required=False, allow_blank=True, allow_null=True
    )
    """
    def __init__(self, *args, **kwargs):
        kwargs['default'] = serializers.empty
        kwargs['required'] = True
        kwargs['allow_blank'] = True
        # This fixes the validation error when the key for an integer field
        # is set in JSON with a value of null.
        kwargs['allow_null'] = True
        super().__init__(*args, **kwargs)


class OptionalDateField(serializers.DateField):
    """
    Initializes a serializers.DateField that is optional.

    This is equivalent to setting a serializer.DateField as such:
    some_optional_date_field = serializers.DateField(
        default=empty, required=False, allow_null=True
    )
    """

    def __init__(self, *args, **kwargs):
        kwargs['default'] = serializers.empty
        kwargs['required'] = False
        # This fixes the validation error when the key for a date field
        # is set in JSON with a value of null.
        kwargs['allow_null'] = True
        super().__init__(*args, **kwargs)


class OptionalDateTimeField(serializers.DateTimeField):
    """
    Initializes a serializers.DateField that is optional.

    This is equivalent to setting a serializer.DateField as such:
    some_optional_date_field = serializers.DateField(
        default=empty, required=False, allow_null=True
    )
    """

    def __init__(self, *args, **kwargs):
        kwargs['default'] = serializers.empty
        kwargs['required'] = False
        # This fixes the validation error when the key for a date field
        # is set in JSON with a value of null.
        kwargs['allow_null'] = True
        super().__init__(*args, **kwargs)

