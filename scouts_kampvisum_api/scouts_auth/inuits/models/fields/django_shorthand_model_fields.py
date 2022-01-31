import warnings, ast
from typing import Iterable

from django.db import models
from django.core.exceptions import ValidationError

from scouts_auth.inuits.models.fields import DatetypeAwareDateField


DEFAULT_CHAR_FIELD_LENGTH = 128


class OptionalCharField(models.CharField):
    """
    Initializes a models.CharField as optional.

    This is equivalent to setting a models.CharField as such:
    some_optional_char_field = models.CharField(
        blank=True,
    )
    If a default value is passed, it is discarded.
    If max_length is not specified, it is set to 128.

    @see https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.Field.null
    """

    def __init__(self, *args, **kwargs):
        if "default" in kwargs:
            default_value = kwargs.pop("default", None)
            warning = "A default value '{}' was passed to {} and was discarded. Use DefaultCharField if this field needs a default.".format(
                default_value, self.__class__.__name__
            )
            warnings.warn(warning)
        if "max_length" not in kwargs:
            kwargs["max_length"] = DEFAULT_CHAR_FIELD_LENGTH
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)


class DefaultCharField(models.CharField):
    """
    Initializes a models.CharField as optional with a default.

    This is equivalent to setting a models.CharField as such:
    some_optional_char_field = models.CharField(
        blank=True, default=<some_default_value>
    )
    If max_length is not specified, it is set to 128.

    @see https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.Field.null
    """

    def __init__(self, *args, **kwargs):
        if "max_length" not in kwargs:
            kwargs["max_length"] = DEFAULT_CHAR_FIELD_LENGTH
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)


class RequiredCharField(models.CharField):
    """
    Initializes a models.CharField as required.

    This is equivalent to setting a models.CharField as such:
    some_required_char_field = models.CharField(
        blank=False,
    )

    @see https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.Field.null
    """

    def __init__(self, *args, **kwargs):
        if "max_length" not in kwargs:
            kwargs["max_length"] = DEFAULT_CHAR_FIELD_LENGTH
        kwargs["blank"] = False
        super().__init__(*args, **kwargs)


class UniqueRequiredCharField(models.CharField):
    """
    Initializes a models.CharField as required and unique.

    This is equivalent to setting a models.CharField as such:
    some_required_char_field = models.CharField(
        blank=False,
    )

    @see https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.Field.null
    """

    def __init__(self, *args, **kwargs):
        if "max_length" not in kwargs:
            kwargs["max_length"] = DEFAULT_CHAR_FIELD_LENGTH
        kwargs["blank"] = False
        kwargs["unique"] = True
        super().__init__(*args, **kwargs)


class OptionalTextField(models.TextField):
    """
    Initializes a models.TextField as optional.

    This is equivalent to setting a models.TextField as such:
    some_optional_char_field = models.TextField(
        blank=True,
    )
    If a default value is passed, it is discarded.

    @see https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.Field.null
    """

    def __init__(self, *args, **kwargs):
        if "default" in kwargs:
            default_value = kwargs.pop("default", None)
            if default_value is not None and len(default_value.strip()) > 0:
                warning = "A default value '{}' was passed to {} and was discarded. Use models.TextField if this field needs a default.".format(
                    default_value, self.__class__.__name__
                )
                warnings.warn(warning)
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)


class OptionalIntegerField(models.IntegerField):
    """
    Initializes a models.IntegerField as optional.

    This is equivalent to setting a models.IntegerField as such:
    some_optional_integer_field = models.IntegerField(
        blank=True,
        null=True,
    )
    If a default value is passed, it is discarded.
    """

    def __init__(self, *args, **kwargs):
        if "default" in kwargs:
            default_value = kwargs.pop("default", None)
            warning = "A default value '{}' was passed to {} and was discarded. Use models.IntegerField if this field needs a default.".format(
                default_value, self.__class__.__name__
            )
            warnings.warn(warning)
        kwargs["blank"] = True
        kwargs["null"] = True
        super().__init__(*args, **kwargs)


class DefaultIntegerField(models.IntegerField):
    """
    Initializes a models.IntegerField as optional with a default.

    This is equivalent to setting a models.IntegerField as such:
    some_optional_integer_field = models.IntegerField(
        blank=True,
        default=<some_default_value>,
    )
    """

    def __init__(self, *args, **kwargs):
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)


class RequiredIntegerField(models.IntegerField):
    """
    Initializes a models.IntegerField as required.

    This is equivalent to setting a models.IntegerField as such:
    some_required_integer_field = models.IntegerField(
        blank=False,
        null=False,
    )
    If a default value is not passed, then a ValidationError is raised.
    """

    def __init__(self, *args, **kwargs):
        if "default" not in kwargs:
            raise ValidationError("A RequiredIntegerField needs a default")
        kwargs["blank"] = False
        kwargs["null"] = False
        super().__init__(*args, **kwargs)


class OptionalEmailField(OptionalCharField):
    """
    Initializes a models.EmailField as optional.

    This is equivalent to setting a models.EmailField as such:
    some_optional_email_field = models.EmailField(
        blank=True,
    )
    If a default value is passed, it is discarded.

    @see https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.Field.null
    """

    def __init__(self, *args, **kwargs):
        if "default" in kwargs:
            default_value = kwargs.pop("default", None)
            if default_value is not None and len(default_value.strip()) > 0:
                warning = "A default value '{}' was passed to {} and was discarded. Use models.EmailField if this field needs a default.".format(
                    default_value, self.__class__.__name__
                )
                warnings.warn(warning)
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)


class OptionalDateField(DatetypeAwareDateField):
    """
    Initializes a models.DateField as optional.

    This is equivalent to setting a models.DateField as such:
    some_optional_date_field = models.DateField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )
    If a default value is passed, it is discarded.
    """

    def __init__(self, *args, **kwargs):
        if "default" in kwargs:
            default_value = kwargs.pop("default", None)
            warning = "A default value '{}' was passed to {} and was discarded. Use models.DateField if this field needs a default.".format(
                default_value, self.__class__.__name__
            )
            warnings.warn(warning)
        kwargs["auto_now"] = False
        kwargs["auto_now_add"] = False
        kwargs["blank"] = True
        kwargs["null"] = True

        super().__init__(*args, **kwargs)


class OptionalDateTimeField(models.DateTimeField):
    """
    Initializes a models.DateField as optional.

    This is equivalent to setting a models.DateField as such:
    some_optional_date_field = models.DateField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )
    If a default value is passed, it is discarded.
    """

    def __init__(self, *args, **kwargs):
        if "default" in kwargs:
            default_value = kwargs.pop("default", None)
            warning = "A default value '{}' was passed to {} and was discarded. Use models.DateTimeField if this field needs a default.".format(
                default_value, self.__class__.__name__
            )
            warnings.warn(warning)
        kwargs["auto_now"] = False
        kwargs["auto_now_add"] = False
        kwargs["blank"] = True
        kwargs["null"] = True

        super().__init__(*args, **kwargs)


class ListField(models.CharField):
    """
    A custom Django field to represent lists as comma separated strings

    @see https://stackoverflow.com/a/53384689
    """

    token = ","

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop("token", ",")
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["token"] = self.token
        return name, path, args, kwargs

    def to_python(self, value):
        if isinstance(value, list):
            return value

        class SubList(list):
            def __init__(self, token, *args):
                self.token = token
                super().__init__(*args)

            def __str__(self):
                return self.token.join(self)

        if value is None:
            return SubList(self.token)

        return SubList(self.token, value.split(self.token))

        return ast.literal_eval(value)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if not value:
            return

        assert isinstance(value, Iterable)

        return self.token.join(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)

        return self.get_prep_value(value)


class OptionalForeignKey(models.ForeignKey):
    """
    Initializes a models.ForeignKey as optional.

    This is equivalent to setting a models.ForeignKey as such:
    some_optional_foreign_key = models.ForeignKey(
        blank=True,
        null=True,
    )
    """

    def __init__(self, *args, **kwargs):
        kwargs["blank"] = True
        kwargs["null"] = True
        super().__init__(*args, **kwargs)
