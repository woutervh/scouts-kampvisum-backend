class BooleanParser:
    @staticmethod
    def to_bool(value: str) -> bool:
        if value is None:
            return False
        if value.lower() in ("true", "True", "yes", "y", "ja", "j"):
            return True
        return False

    @staticmethod
    def to_str(value: bool, boolean_true: str = "YES", boolean_false: str = "NO") -> str:
        if value is None:
            return boolean_false
        if value:
            return boolean_true
        return boolean_false

    @staticmethod
    def to_char(value: bool, boolean_true: str = "Y", boolean_false: str = "N") -> str:
        boolean_value = BooleanParser.to_str(value, boolean_true, boolean_false)

        return boolean_value[0]
