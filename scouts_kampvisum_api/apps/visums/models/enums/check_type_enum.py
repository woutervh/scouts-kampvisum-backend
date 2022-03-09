from django.db import models


class CheckTypeEnum(models.TextChoices):
    """
    An enum that links known models to a routable endpoint string
    """

    SIMPLE_CHECK = "SimpleCheck", "simple"
    DATE_CHECK = "DateCheck", "date"
    DURATION_CHECK = "DurationCheck", "duration"
    LOCATION_CHECK = "LocationCheck", "location"
    CAMP_LOCATION_CHECK = "CampLocationCheck", "camp_location"
    MEMBER_CHECK = "MemberCheck", "member"
    PARTICIPANT_CHECK = "ParticipantCheck", "participant"
    PARTICIPANT_MEMBER_CHECK = "ParticipantMemberCheck", "participant"
    PARTICIPANT_COOK_CHECK = "ParticipantCookCheck", "participant"
    PARTICIPANT_LEADER_CHECK = "ParticipantLeaderCheck", "participant"
    PARTICIPANT_RESPONSIBLE_CHECK = (
        "ParticipantResponsibleCheck",
        "participant",
    )
    PARTICIPANT_ADULT_CHECK = "ParticipantAdultCheck", "participant"
    COMMENT_CHECK = "CommentCheck", "comment"
    FILE_UPLOAD_CHECK = "FileUploadCheck", "file"
    NUMBER_CHECK = "NumberCheck", "number"

    @staticmethod
    def endpoint_from_type(check_type: str):
        for option in CheckTypeEnum.choices:
            if option[0] == check_type:
                return option[1]
        return None
