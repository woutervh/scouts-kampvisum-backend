class AbstractScoutsGrouping:

    name: str
    index: int

    def __init__(self, name: str = "", index: int = -1):
        self.name = name
        self.index = index

    def __str__(self):
        return "name({}), index({})".format(self.name, self.index)
