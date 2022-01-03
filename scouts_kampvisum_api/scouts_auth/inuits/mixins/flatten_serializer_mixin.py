import logging, uuid


logger = logging.getLogger(__name__)


class FlattenSerializerMixin(object):
    """
    Flatten nested serializer data by adding a flatten property in Meta

    @see https://stackoverflow.com/a/41418576
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_representation(self, obj):
        """
        Move fields from nested serializers to root if Meta.flatten is set
        """
        representation = super().to_representation(obj)

        if hasattr(self.Meta, "flatten"):
            for field, serializer_class in self.Meta.flatten:
                logger.debug(
                    "Serializer OUTPUT: Flattening field %s with serializer %s",
                    field,
                    serializer_class.__name__,
                )
                serializer = serializer_class(context=self.context)
                objrep = serializer.to_representation(getattr(obj, field))

                for key in objrep:
                    if key in representation:
                        representation[field + "__" + key] = objrep[key]
                    else:
                        representation[key] = objrep[key]

        return representation

    # @TODO: find a way to distinguish between input create and input serialization, so that pk fields etc are ignored
    def to_internal_value(self, data):
        if not isinstance(data, dict):
            return
        logger.debug("Serializer INPUT data: %s (%s)", data, type(data).__name__)

        is_input_serializer = (
            True
            if hasattr(self.Meta, "input_serializer") and self.Meta.input_serializer
            else False
        )

        # remove flattened nested keys
        nested_fields = {}
        if hasattr(self.Meta, "flatten"):
            for field, serializer_class in self.Meta.flatten:
                logger.debug(
                    "Serializer INPUT: Flattening field %s with serializer %s",
                    field,
                    serializer_class.__name__,
                )
                serializer = serializer_class(context=self.context)
                serializer_fields = serializer.get_fields()
                serializer_internal = {}
                if is_input_serializer:
                    serializer_fields["id"] = uuid.uuid4()
                    serializer_internal
                for key in serializer_fields:
                    if key in data:
                        serializer_internal[key] = data.pop(key)
                nested_fields[field] = serializer_internal

        for key in nested_fields:
            logger.debug("Append value %s to key %s", nested_fields[key], key)
            data[key] = nested_fields[key]
        internal_values = super().to_internal_value(data)

        logger.debug("Internal values: %s", internal_values)

        return internal_values
