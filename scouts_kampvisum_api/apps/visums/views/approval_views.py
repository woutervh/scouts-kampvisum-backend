from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.visums.models import LinkedCategory, LinkedSubCategory


class ApprovalViewSet(viewsets.GenericViewSet):
    def partial_update_feedback(self, request, linked_sub_category_id):
        linked_sub_category: LinkedSubCategory = LinkedSubCategory.objects.safe_get(
            id=linked_sub_category_id, raise_error=True
        )

        return Response({}, status=status.HTTP_201_CREATED)

    def partial_update_approval(self, request, linked_sub_category_id):
        linked_sub_category: LinkedSubCategory = LinkedSubCategory.objects.safe_get(
            id=linked_sub_category_id, raise_error=True
        )

        return Response({}, status=status.HTTP_201_CREATED)

    def partial_update_notes(self, request, linked_category_id):
        linked_category: LinkedCategory = LinkedCategory.objects.safe_get(
            id=linked_category_id, raise_error=True
        )

        return Response({}, status=status.HTTP_201_CREATED)
