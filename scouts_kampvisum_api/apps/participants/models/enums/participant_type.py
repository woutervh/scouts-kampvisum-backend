from django.db import models


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


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
    def parse_participant_type(participant_type: str = None) -> bool:
        if not participant_type:
            return ParticipantType.PARTICIPANT

        participant_type = participant_type.upper()

        for option in ParticipantType.choices:
            if option[0] == participant_type or option[1] == participant_type.lower():
                return option
        return None

    @staticmethod
    def _is_type(participant_type: any = None, compare=None) -> bool:
        if not participant_type or not compare:
            return False
        logger.debug(
            "TYPE: %s (%s) - COMPARE: %s (%s)",
            participant_type,
            type(participant_type).__name__,
            compare,
            type(compare).__name__,
        )

        if (
            isinstance(participant_type, str)
            and ParticipantType.parse_participant_type(participant_type) == compare
        ):
            return True

        if (
            isinstance(participant_type, tuple)
            and participant_type[0].upper() == compare
            or participant_type[1].lower == compare
        ):
            return True

        return False

    @staticmethod
    def is_participant(participant_type: any = None) -> bool:
        return ParticipantType._is_type(participant_type, ParticipantType.PARTICIPANT)

    @staticmethod
    def is_member(participant_type: any = None) -> bool:
        return ParticipantType._is_type(participant_type, ParticipantType.MEMBER)

    @staticmethod
    def is_cook(participant_type: any = None) -> bool:
        return ParticipantType._is_type(participant_type, ParticipantType.COOK)

    @staticmethod
    def is_leader(participant_type: any = None) -> bool:
        return ParticipantType._is_type(participant_type, ParticipantType.LEADER)

    @staticmethod
    def is_responsible(participant_type: any = None) -> bool:
        return ParticipantType._is_type(participant_type, ParticipantType.RESPONSIBLE)

    @staticmethod
    def is_adult(participant_type: any = None) -> bool:
        return ParticipantType._is_type(participant_type, ParticipantType.ADULT)
