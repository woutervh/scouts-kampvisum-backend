import copy, uuid


def is_non_empty(value: str) -> bool:
    """Checks if a value is a string and contains non-whitespace chars"""
    if value is not None and isinstance(value, str) and len(value.strip()) > 0:
        return True

    return False


def copy_basemodel(instance):
    instance_copy = copy.deepcopy(instance)

    instance_copy.id = None
    instance_copy.uuid = uuid.uuid4()

    return instance_copy
