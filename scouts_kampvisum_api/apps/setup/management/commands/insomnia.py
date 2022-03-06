import json, datetime, uuid
from types import SimpleNamespace

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.camps.models import Camp, CampYear, CampType

from apps.groups.models import ScoutsSectionName, ScoutsSection, ScoutsGroupType

from apps.participants.models import InuitsParticipant
from apps.participants.services import InuitsParticipantService

from apps.visums.models import (
    CampVisum,
    Category,
    SubCategory,
    Check,
    LinkedCategory,
    LinkedSubCategory,
    LinkedCheck,
    LinkedSimpleCheck,
    LinkedDurationCheck,
    LinkedLocationCheck,
    LinkedParticipantCheck,
    LinkedCommentCheck,
    LinkedFileUploadCheck,
    LinkedNumberCheck,
)
from apps.visums.services import LinkedCheckService

from apps.deadlines.models import (
    Deadline,
    DeadlineFlag,
)

from scouts_auth.groupadmin.models import ScoutsUser

from scouts_auth.inuits.models import PersistedFile, Gender
from scouts_auth.inuits.services import PersistedFileService

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Provides some known uuids for insomnia"
    exception = False

    def handle(self, *args, **kwargs):
        user = self.setup_admin_user()

        data = dict()

        # ScoutsSectionName
        data["scouts_section_name_first"] = str(ScoutsSectionName.objects.first().id)
        data["scouts_section_name_last"] = str(ScoutsSectionName.objects.last().id)
        data["scouts_section_name_kapoenen"] = str(
            ScoutsSectionName.objects.safe_get(name="kapoenen", gender=Gender.MIXED).id
        )
        data["scouts_section_name_welpen"] = str(
            ScoutsSectionName.objects.safe_get(
                name="kabouters en welpen", gender=Gender.MIXED
            ).id
        )
        # ScoutsSection
        data["scouts_section_first"] = str(ScoutsSection.objects.first().id)
        data["scouts_section_last"] = str(ScoutsSection.objects.last().id)
        # ScoutsSection
        data["scouts_group_type_first"] = str(ScoutsGroupType.objects.first().id)
        data["scouts_group_type_last"] = str(ScoutsGroupType.objects.last().id)
        # Year
        data["current_year"] = str(datetime.datetime.now().year)
        data["next_year"] = str(int(data.get("current_year")) + 1)
        # CampYear
        data["camp_year_first"] = str(CampYear.objects.first().id)
        data["camp_year_last"] = str(CampYear.objects.last().id)
        data["camp_year_current"] = str(
            CampYear.objects.filter(year=datetime.datetime.now().year).first().id
        )
        # Camp
        data["camp_first"] = str(Camp.objects.first().id)
        data["camp_last"] = str(Camp.objects.last().id)
        # PersistedFile
        service = PersistedFileService()
        service.save_local_file("initial_data/test/menu.pdf")
        service.save_local_file("initial_data/test/planning.pdf")
        data["file_first"] = str(PersistedFile.objects.first().id)
        data["file_last"] = str(PersistedFile.objects.last().id)
        # NonMember
        self.add_non_members(user)
        data["participant_non_member_first"] = str(
            InuitsParticipant.objects.filter(is_member=False).first().id
        )
        data["participant_non_member_last"] = str(
            InuitsParticipant.objects.filter(is_member=False).last().id
        )
        # GA member
        data["ga_member_jeroen_budts"] = "5e19c7d0-d448-4c08-ab37-5a20a9054101"
        data["ga_member_jeroen_wouters"] = "1f59774b-e89b-4617-aa7e-2e55fb1045b0"
        data["ga_member_ricardo_acosta_torres"] = "5b4bda13-df27-45f6-bd9c-d7d22a5f7d07"
        data["ga_member_stijn_verholen"] = "b91ba6e9-ab51-49ce-86e8-e77a7224971e"
        # CampType
        data["camp_type_first"] = str(CampType.objects.first().id)
        data["camp_type_last"] = str(CampType.objects.last().id)
        # Category
        data["category_first"] = str(Category.objects.first().id)
        data["category_last"] = str(Category.objects.last().id)
        # SubCategory
        data["sub_category_first"] = str(SubCategory.objects.first().id)
        data["sub_category_last"] = str(SubCategory.objects.last().id)
        # Check
        data["check_first"] = str(Check.objects.first().id)
        data["check_last"] = str(Check.objects.last().id)
        # Visum
        data["visum_first"] = str(CampVisum.objects.first().id)
        data["visum_last"] = str(CampVisum.objects.last().id)
        # LinkedCategory
        data["linked_category_first"] = str(LinkedCategory.objects.first().id)
        data["linked_category_last"] = str(LinkedCategory.objects.last().id)
        # LinkedSubCategory
        data["linked_sub_category_first"] = str(LinkedSubCategory.objects.first().id)
        data["linked_sub_category_last"] = str(LinkedSubCategory.objects.last().id)
        # LinkedCheck
        data["linked_check_first"] = str(LinkedCheck.objects.first().id)
        data["linked_check_last"] = str(LinkedCheck.objects.last().id)
        # SimpleCheck
        data["linked_check_simple_first"] = str(LinkedSimpleCheck.objects.first().id)
        data["linked_check_simple_last"] = str(LinkedSimpleCheck.objects.last().id)
        # DateCheck
        # data["linked_check_date_first"] = str(LinkedDateCheck.objects.first().id)
        # data["linked_check_date_last"] = str(LinkedDateCheck.objects.last().id)
        # DurationCheck
        data["linked_check_duration_first"] = str(
            LinkedDurationCheck.objects.first().id
        )
        data["linked_check_duration_last"] = str(LinkedDurationCheck.objects.last().id)
        # LocationCheck
        data["linked_check_location_first"] = str(
            LinkedLocationCheck.objects.filter(is_camp_location=False).first().id
        )
        data["linked_check_location_last"] = str(
            LinkedLocationCheck.objects.filter(is_camp_location=False).last().id
        )
        # CampLocationCheck
        data["linked_check_camp_location_first"] = str(
            LinkedLocationCheck.objects.filter(is_camp_location=True).first().id
        )
        data["linked_check_camp_location_last"] = str(
            LinkedLocationCheck.objects.filter(is_camp_location=True).last().id
        )
        # MemberCheck
        data["linked_check_member_first"] = str(
            LinkedParticipantCheck.objects.filter(parent__is_member=True).first().id
        )
        data["linked_check_member_last"] = str(
            LinkedParticipantCheck.objects.filter(parent__is_member=True).last().id
        )
        data["linked_check_participant_first"] = str(
            LinkedParticipantCheck.objects.filter(parent__is_member=False).first().id
        )
        data["linked_check_participant_last"] = str(
            LinkedParticipantCheck.objects.filter(parent__is_member=False).last().id
        )
        # ParticipantCheck
        data["linked_check_participant_ombudsman"] = str(
            LinkedParticipantCheck.objects.filter(
                parent__name="communication_agreements_parents_ombudsman_contact"
            )
            .first()
            .id
        )
        # CommentCheck
        data["linked_check_comment_first"] = str(LinkedCommentCheck.objects.first().id)
        data["linked_check_comment_last"] = str(LinkedCommentCheck.objects.last().id)
        # NumberCheck
        data["linked_check_number_first"] = str(LinkedNumberCheck.objects.first().id)
        data["linked_check_number_last"] = str(LinkedNumberCheck.objects.last().id)
        # FileUploadCheck
        data["linked_check_file_upload_first"] = str(
            LinkedFileUploadCheck.objects.first().id
        )
        data["linked_check_file_upload_last"] = str(
            LinkedFileUploadCheck.objects.last().id
        )

        # Deadline
        data["deadline_first"] = str(Deadline.objects.first().id)
        data["deadline_last"] = str(Deadline.objects.last().id)
        # LinkedSubCategoryDeadline
        # data["sub_category_deadline_first"] = str(
        #     LinkedSubCategoryDeadline.objects.first().id
        # )
        # data["sub_category_deadline_last"] = str(
        #     LinkedSubCategoryDeadline.objects.last().id
        # )
        # # LinkedCheckDeadline
        # data["check_category_deadline_first"] = str(
        #     LinkedCheckDeadline.objects.first().id
        # )
        # data["check_category_deadline_last"] = str(
        #     LinkedCheckDeadline.objects.last().id
        # )
        # # MixedDeadline
        # data["mixed_deadline_first"] = str(MixedDeadline.objects.first().id)
        # data["mixed_deadline_last"] = str(MixedDeadline.objects.last().id)
        # DeadlineFlag
        data["deadline_flag_first"] = str(DeadlineFlag.objects.first().id)
        data["deadline_flag_last"] = str(DeadlineFlag.objects.last().id)

        data["visum_participant_first"] = str(
            self.link_participant(
                user,
                data["linked_check_participant_first"],
                data["participant_non_member_first"],
            )
        )
        data["visum_participant_last"] = str(
            self.link_participant(
                user,
                data["linked_check_participant_last"],
                data["participant_non_member_last"],
            )
        )

        print(json.dumps(data, indent=2))

    def setup_admin_user(self):
        try:
            return ScoutsUser.objects.get(username="ADMIN")
        except:
            user: ScoutsUser = ScoutsUser()

            user.group_admin_id = uuid.uuid4()
            user.gender = "M"
            user.phone_number = ""
            user.membership_number = ""
            user.customer_number = ""
            user.birth_date = datetime.datetime.now()
            user.access_token = ""

            user.username = "ADMIN"
            user.first_name = "admin"
            user.last_name = "admin"
            user.email = "boro@inuits.eu"
            user.password = ScoutsUser.objects.make_random_password(length=128)

            user.full_clean()
            user.save()

            return user

    def add_non_members(self, user: settings.AUTH_USER_MODEL):
        service = InuitsParticipantService()

        self.add_non_member(
            user,
            service,
            InuitsParticipant(
                group_group_admin_id="X9002G",
                first_name="Jeroen1",
                last_name="Achternaam1",
                phone_number="+3231111111",
                cell_number="+3231111111",
                email="jeroen1.achternaam1@email.be",
                birth_date="2001-01-01",
                gender="M",
                street="Straat1",
                number="Nr1",
                letter_box="Bus1",
                postal_code="1000",
                city="BRUSSEL",
            ),
        )

        self.add_non_member(
            user,
            service,
            InuitsParticipant(
                group_group_admin_id="X9002G",
                first_name="Jeroen2",
                last_name="Achternaam2",
                phone_number="+3232222222",
                cell_number="+3232222222",
                email="jeroen2.achternaam2@email.be",
                birth_date="2002-02-02",
                gender="M",
                street="Straat2",
                number="Nr2",
                letter_box="Bus2",
                postal_code="1020",
                city="BRUSSEL",
            ),
        )
        self.add_non_member(
            user,
            service,
            InuitsParticipant(
                group_group_admin_id="X9002G",
                first_name="Jeroen3",
                last_name="Achternaam3",
                phone_number="+3233333333",
                cell_number="+323333333",
                email="jeroen3.achternaam3@email.be",
                birth_date="2003-03-03",
                gender="M",
                street="Straat3",
                number="Nr3",
                letter_box="Bus3",
                postal_code="1030",
                city="BRUSSEL",
            ),
        )

    def add_non_member(
        self,
        user: settings.AUTH_USER_MODEL,
        service: InuitsParticipantService,
        participant: InuitsParticipant,
    ) -> InuitsParticipant:

        return service.create_or_update_participant(
            participant=participant,
            user=user,
            skip_validation=True,
        )

    def link_participant(
        self, user: settings.AUTH_USER_MODEL, check_id, inuits_participant_id
    ):
        service = LinkedCheckService()

        check: LinkedParticipantCheck = LinkedParticipantCheck.objects.get(id=check_id)
        check: LinkedParticipantCheck = service.update_participant_check(
            request=SimpleNamespace(user=user),
            instance=check,
            **{
                "participants": [
                    {"participant": InuitsParticipant(id=inuits_participant_id)}
                ]
            }
        )

        return check.participants.first().id
