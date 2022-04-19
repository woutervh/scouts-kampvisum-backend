from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.visums.models import CampVisum, LinkedSubCategory
from apps.visums.models.enums import CampVisumApprovalState
from apps.visums.serializers import (
    LinkedSubCategorySerializer,
    LinkedSubCategoryFeedbackSerializer,
    LinkedSubCategoryApprovalSerializer,
    CampVisumSerializer,
    CampVisumNotesSerializer,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ApprovalViewSet(viewsets.GenericViewSet):
    def partial_update_feedback(self, request, linked_sub_category_id):
        instance: LinkedSubCategory = LinkedSubCategory.objects.safe_get(
            id=linked_sub_category_id, raise_error=True
        )

        logger.debug("FEEDBACK UPDATE REQUEST DATA: %s", request.data)

        serializer = LinkedSubCategoryFeedbackSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("FEEDBACK UPDATE VALIDATED DATA: %s", validated_data)

        instance.feedback = validated_data.get("feedback")

        logger.debug(
            "Setting feedback on LinkedSubCategory %s (%s)",
            instance.parent.name,
            instance.id,
        )

        instance.full_clean()
        instance.save()

        output_serializer = LinkedSubCategorySerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update_approval(self, request, linked_sub_category_id):
        instance: LinkedSubCategory = LinkedSubCategory.objects.safe_get(
            id=linked_sub_category_id, raise_error=True
        )

        logger.debug("APPROVAL UPDATE REQUEST DATA: %s", request.data)

        serializer = LinkedSubCategoryApprovalSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("APPROVAL UPDATE VALIDATED DATA: %s", validated_data)

        approval: CampVisumApprovalState = CampVisumApprovalState.get_state(
            validated_data.get("approval")
        )

        logger.debug(
            "Setting approval state %s (%s) on LinkedSubCategory %s (%s)",
            approval[1],
            approval[0],
            instance.parent.name,
            instance.id,
        )

        instance.approval = approval[0]

        instance.full_clean()
        instance.save()

        output_serializer = LinkedSubCategorySerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update_notes(self, request, visum_id):
        instance: CampVisum = CampVisum.objects.safe_get(id=visum_id, raise_error=True)

        logger.debug("DC NOTES UPDATE REQUEST DATA: %s", request.data)

        serializer = CampVisumNotesSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("DC NOTES UPDATE VALIDATED DATA: %s", validated_data)

        notes = validated_data.get("notes")

        logger.debug(
            "Adding DC notes on CampVisum %s (%s)",
            instance.camp.name,
            instance.id,
        )

        instance.notes = notes

        instance.full_clean()
        instance.save()

        output_serializer = CampVisumSerializer(instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
