import logging, json, datetime

from django.core.management.base import BaseCommand


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Provides some known uuids for insomnia"
    exception = False

    def handle(self, *args, **kwargs):
        from apps.camps.models import Camp, CampYear
        from apps.groups.models import ScoutsSectionName, ScoutsSection, ScoutsGroupType
        from apps.people.models import InuitsNonMember
        from apps.visums.models import (
            CampVisum,
            CampYearCategorySet,
            CategorySet,
            Category,
            SubCategory,
            Check,
            LinkedCategory,
            LinkedSubCategory,
            LinkedCheck,
            LinkedSimpleCheck,
            LinkedDateCheck,
            LinkedDurationCheck,
            LinkedLocationCheck,
            LinkedMemberCheck,
            LinkedCommentCheck,
            LinkedFileUploadCheck,
        )

        data = dict()

        # ScoutsSectionName
        data["scouts_section_name_first"] = str(ScoutsSectionName.objects.first().id)
        data["scouts_section_name_last"] = str(ScoutsSectionName.objects.last().id)
        # ScoutsSection
        data["scouts_section_first"] = str(ScoutsSection.objects.first().id)
        data["scouts_section_last"] = str(ScoutsSection.objects.last().id)
        # ScoutsSection
        data["scouts_group_type_first"] = str(ScoutsGroupType.objects.first().id)
        data["scouts_group_type_last"] = str(ScoutsGroupType.objects.last().id)
        # Year
        data["current_year"] = str(datetime.datetime.now().year)
        data["next_year"] = str(int(data.get("current_year")) + 1)
        # Camp
        data["camp_year_first"] = str(CampYear.objects.first().id)
        data["camp_year_last"] = str(CampYear.objects.last().id)
        data["camp_year_current"] = str(
            CampYear.objects.filter(year=datetime.datetime.now().year).first().id
        )
        # Camp
        data["camp_first"] = str(Camp.objects.first().id)
        data["camp_last"] = str(Camp.objects.last().id)
        # NonMember
        # data["non_member_first"] = str(InuitsNonMember.objects.first().id)
        # data["non_member_last"] = str(InuitsNonMember.objects.last().id)
        # CategorySet
        data["camp_year_category_set_first"] = str(
            CampYearCategorySet.objects.first().id
        )
        data["camp_year_category_set_last"] = str(CampYearCategorySet.objects.last().id)
        # CategorySet
        data["category_set_first"] = str(CategorySet.objects.first().id)
        data["category_set_last"] = str(CategorySet.objects.last().id)
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
            LinkedLocationCheck.objects.first().id
        )
        data["linked_check_location_last"] = str(LinkedLocationCheck.objects.last().id)
        # MemberCheck
        data["linked_check_member_first"] = str(LinkedMemberCheck.objects.first().id)
        data["linked_check_member_last"] = str(LinkedMemberCheck.objects.last().id)
        # CommentCheck
        data["linked_check_comment_first"] = str(LinkedCommentCheck.objects.first().id)
        data["linked_check_comment_last"] = str(LinkedCommentCheck.objects.last().id)
        # FileUploadCheck
        data["linked_check_file_upload_first"] = str(
            LinkedFileUploadCheck.objects.first().id
        )
        data["linked_check_file_upload_last"] = str(
            LinkedFileUploadCheck.objects.last().id
        )

        print(json.dumps(data, indent=2))
