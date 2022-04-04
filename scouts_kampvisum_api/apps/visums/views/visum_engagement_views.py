from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.visums.models import CampVisumEngagement
from apps.visums.serializers import CampVisumEngagementSerializer
from apps.visums.services import CampVisumEngagementService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumEngagementViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing camp instances.
    """

    serializer_class = CampVisumEngagementSerializer
    queryset = CampVisumEngagement.objects.all()

    camp_visum_approval_service = CampVisumEngagementService()

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampVisumEngagementSerializer})
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = CampVisumEngagementSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CampVisumEngagementSerializer,
        responses={status.HTTP_200_OK: CampVisumEngagementSerializer},
    )
    def partial_update(self, request, pk=None):
        instance = CampVisumEngagement.objects.safe_get(pk=pk, raise_error=True)

        logger.debug("CAMP VISUM APPROVAL UPDATE REQUEST DATA: %s", request.data)
        
        data = request.data
        data["id"] = pk

        serializer = CampVisumEngagementSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CAMP VISUM APPROVAL UPDATE VALIDATED DATA: %s", validated_data)

        updated_instance = self.camp_visum_approval_service.update_engagement(
            request, instance=instance, **validated_data
        )

        output_serializer = CampVisumEngagementSerializer(
            updated_instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)
