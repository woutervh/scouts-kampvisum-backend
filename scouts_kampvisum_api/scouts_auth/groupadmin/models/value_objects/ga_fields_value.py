class AbstractScoutsValue:

    key: str
    value: str

    def __init__(self, key: str = "", value: str = ""):
        self.key = key
        self.value = value

    def __str__(self):
        return "[key({}), value({})]".format(self.key, self.value)
