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
    def parse_participant_type(participant_type: str = None):
        if not participant_type:
            return ParticipantType.PARTICIPANT

        for option in ParticipantType.choices:
            if option[0] == participant_type:
                return option
        return None
