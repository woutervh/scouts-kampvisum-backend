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
from apps.visums.services import CampVisumApprovalService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumApprovalViewSet(viewsets.GenericViewSet):

    approval_service = CampVisumApprovalService()

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

        instance = self.approval_service.update_feedback(
            request=request, instance=instance, feedback=validated_data.get("feedback")
        )

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

        instance = self.approval_service.update_approval(
            request=request, instance=instance, approval=validated_data.get("approval")
        )

        output_serializer = LinkedSubCategorySerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def global_update_approval(self, request, visum_id):
        instance: CampVisum = CampVisum.objects.safe_get(id=visum_id, raise_error=True)

        instance = self.approval_service.global_update_approval(
            request=request, instance=instance
        )

        output_serializer = CampVisumSerializer(instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def global_update_disapproval(self, request, visum_id):
        instance: CampVisum = CampVisum.objects.safe_get(id=visum_id, raise_error=True)

        instance = self.approval_service.global_update_approval(
            request=request,
            instance=instance,
            approval=CampVisumApprovalState.DISAPPROVED,
        )

        output_serializer = CampVisumSerializer(instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update_dc_notes(self, request, visum_id):
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

        instance = self.approval_service.update_dc_notes(
            request=request, instance=instance, notes=validated_data.get("notes")
        )

        output_serializer = CampVisumSerializer(instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def handle_feedback(self, request, linked_sub_category_id):
        instance: LinkedSubCategory = LinkedSubCategory.objects.safe_get(
            id=linked_sub_category_id, raise_error=True
        )

        instance = self.approval_service.handle_feedback(
            request=request, instance=instance
        )

        output_serializer = LinkedSubCategorySerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def global_handle_feedback(self, request, visum_id):
        instance: CampVisum = CampVisum.objects.safe_get(id=visum_id, raise_error=True)

        instance = self.approval_service.global_handle_feedback(
            request=request, instance=instance
        )

        output_serializer = CampVisumSerializer(instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
