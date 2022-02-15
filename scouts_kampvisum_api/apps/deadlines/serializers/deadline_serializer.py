import logging

from rest_framework import serializers

from apps.deadlines.models import (
    Deadline,
    LinkedSubCategoryDeadline,
    LinkedCheckDeadline,
    MixedDeadline,
)
from apps.deadlines.models.enums import DeadlineType
from apps.deadlines.serializers import DefaultDeadlineSerializer

from apps.visums.models import LinkedSubCategory, LinkedCheck
from apps.visums.models.enums import CheckState
from apps.visums.serializers import (
    CampVisumSerializer,
    LinkedSubCategorySerializer,
    LinkedCheckSerializer,
)


logger = logging.getLogger(__name__)


class DeadlineSerializer(serializers.ModelSerializer):

    parent = DefaultDeadlineSerializer(required=False)
    visum = CampVisumSerializer(required=False)

    class Meta:
        model = Deadline
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        # logger.debug("DEADLINE SERIALIZER TO_INTERNAL_VALUE: %s", data)

        data["deadline_type"] = DeadlineType.DEADLINE

        return data

    def to_representation(self, obj: Deadline) -> dict:
        data = super().to_representation(obj)

        visum = data.pop("visum")
        data["visum"] = visum.get("id")

        return data


class LinkedSubCategoryDeadlineSerializer(DeadlineSerializer):

    linked_sub_categories = LinkedSubCategorySerializer(many=True)

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
        logger.debug("LINKED SUB CATEGORY DEADELINE: %s", data)
        linked_sub_categories = data.get("linked_sub_categories", [])
        results = []
        for linked_sub_category in linked_sub_categories:
            id = linked_sub_category.get("id", None)
            if id:
                instance = LinkedSubCategory.objects.safe_get(id=id)
                if instance:
                    results.append(
                        {
                            "id": instance.category.id,
                            "name": instance.category.parent.name,
                            "label": instance.category.parent.label,
                            "state": linked_sub_category.get(
                                "state", CheckState.UNCHECKED
                            ),
                        }
                    )

        data["linked_sub_categories"] = results

        return data


class LinkedCheckDeadlineSerializer(DeadlineSerializer):

    linked_checks = LinkedCheckSerializer(many=True)

    class Meta:
        model = LinkedCheckDeadline
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        data["deadline_type"] = DeadlineType.LINKED_CHECK

        data = super().to_internal_value(data)

        return data

    def to_representation(self, obj: LinkedCheckDeadline) -> dict:
        data = super().to_representation(obj)

        linked_checks = data.get("linked_checks", {})
        results = []
        for linked_check in linked_checks:
            id = linked_check.get("id", None)
            if id:
                instance = LinkedCheck.objects.safe_get(id=id)
                if instance:
                    results.append(
                        {
                            "id": instance.sub_category.category.id,
                            "name": instance.sub_category.category.parent.name,
                            "label": instance.sub_category.category.parent.label,
                            "state": linked_check.get("state", CheckState.UNCHECKED),
                        }
                    )

        data["linked_checks"] = results

        return data


class MixedDeadlineSerializer(DeadlineSerializer):

    linked_sub_categories = LinkedSubCategorySerializer(many=True)
    linked_checks = LinkedCheckSerializer(many=True)

    class Meta:
        model = MixedDeadline
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        data["deadline_type"] = DeadlineType.LINKED_CHECK

        data = super().to_internal_value(data)

        return data

    def to_representation(self, obj: LinkedCheckDeadline) -> dict:
        data = super().to_representation(obj)

        linked_sub_categories = data.get("linked_sub_categories", [])
        results = []
        for linked_sub_category in linked_sub_categories:
            id = linked_sub_category.get("id", None)
            if id:
                instance = LinkedSubCategory.objects.safe_get(id=id)
                if instance:
                    results.append(
                        {
                            "id": instance.category.id,
                            "name": instance.category.parent.name,
                            "label": instance.category.parent.label,
                            "state": linked_sub_category.get(
                                "state", CheckState.UNCHECKED
                            ),
                        }
                    )

        data["linked_sub_categories"] = results

        linked_checks = data.get("linked_checks", {})
        results = []
        for linked_check in linked_checks:
            id = linked_check.get("id", None)
            if id:
                instance = LinkedCheck.objects.safe_get(id=id)
                if instance:
                    results.append(
                        {
                            "id": instance.sub_category.category.id,
                            "name": instance.sub_category.category.parent.name,
                            "label": instance.sub_category.category.parent.label,
                            "state": linked_check.get("state", CheckState.UNCHECKED),
                        }
                    )

        data["linked_checks"] = results

        return data
