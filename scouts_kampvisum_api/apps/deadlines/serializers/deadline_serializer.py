import logging

from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.deadlines.models import (
    Deadline,
    LinkedSubCategoryDeadline,
    LinkedCheckDeadline,
    DeadlineDependentDeadline,
)
from apps.deadlines.models.enums import DeadlineType
from apps.deadlines.serializers import DeadlineDateSerializer

from apps.visums.models import LinkedSubCategory, LinkedCheck
from apps.visums.serializers import (
    CampVisumSerializer,
    LinkedSubCategorySerializer,
    LinkedCheckSerializer,
)


logger = logging.getLogger(__name__)


class DeadlineSerializer(serializers.ModelSerializer):

    visum = CampVisumSerializer(required=False)
    due_date = DeadlineDateSerializer(required=False)

    class Meta:
        model = Deadline
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        # logger.debug("DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)

        data["deadline_type"] = DeadlineType.DEADLINE

        # visum_id = data.get("visum", {}).get("id", None)
        # if not visum_id:
        #     raise ValidationError("Visum identifier must be provided")

        # visum = CampVisum.objects.safe_get(id=visum_id)
        # if not visum:
        #     raise ValidationError("Invalid id for CampVisum instance: {}".format(visum_id))

        # data["visum"] = CampVisumSerializer(visum).data

        # data = super().to_internal_value(data)

        # logger.debug("DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)

        return data

    def to_representation(self, obj: Deadline) -> dict:
        data = super().to_representation(obj)

        visum = data.pop("visum")
        data["visum"] = visum.get("id")

        return data


class LinkedSubCategoryDeadlineSerializer(DeadlineSerializer):

    linked_sub_category = LinkedSubCategorySerializer()

    class Meta:
        model = LinkedSubCategoryDeadline
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        # logger.debug("SUB CATEGORY DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)

        data["deadline_type"] = DeadlineType.LINKED_SUB_CATEGORY

        data = super().to_internal_value(data)

        return data

    def to_representation(self, obj: LinkedSubCategoryDeadline) -> dict:
        data = super().to_representation(obj)

        # sub_category = data.pop("deadline_sub_category")
        # data["deadline_sub_category"] = sub_category.get("id")
        sub_category = data.get("linked_sub_category", {}).get("id", None)
        if sub_category:
            sub_category = LinkedSubCategory.objects.safe_get(id=sub_category)
            if sub_category:
                category_data = dict()

                category_data["id"] = sub_category.category.id
                category_data["name"] = sub_category.category.parent.name
                category_data["label"] = sub_category.category.parent.label

                data["linked_sub_category"]["category"] = category_data

        return data


class LinkedCheckDeadlineSerializer(DeadlineSerializer):

    linked_check = LinkedCheckSerializer()

    class Meta:
        model = LinkedCheckDeadline
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        data["deadline_type"] = DeadlineType.LINKED_CHECK

        data = super().to_internal_value(data)

        return data

    def to_representation(self, obj: LinkedCheckDeadline) -> dict:
        data = super().to_representation(obj)

        # check = data.pop("deadline_check")
        # data["deadline_check"] = check.get("id")
        check = data.get("linked_check", {}).get("id", None)
        if check:
            check = LinkedCheck.objects.safe_get(id=check)
            if check:
                category_data = dict()

                category_data["id"] = check.sub_category.category.id
                category_data["name"] = check.sub_category.category.parent.name
                category_data["label"] = check.sub_category.category.parent.label

                data["linked_check"]["category"] = category_data

        return data


class DeadlineDependentDeadlineSerializer(DeadlineSerializer):

    deadline_due_after_deadline = DeadlineSerializer()

    class Meta:
        model = DeadlineDependentDeadline
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        data = super().to_internal_value(data)

        return data
