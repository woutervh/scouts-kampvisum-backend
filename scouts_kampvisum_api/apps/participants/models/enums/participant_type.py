from django.db import models


class ParticipantType(models.TextChoices):
    """
    An enum that links known models to a routable endpoint string
    """

    PARTICIPANT = "P", "participant"
    MEMBER = "M", "member"
    COOK = "C", "cook"
    LEADER = "L", "leader"
    RESPONSIBLE = (
        "R",
        "responsible",
    )
    ADULT = "A", "adult"

    @staticmethod
    def endpoint_from_type(check_type: str):
        for option in ParticipantType.choices:
            if option[0] == check_type:
                return option[1]
        return None
