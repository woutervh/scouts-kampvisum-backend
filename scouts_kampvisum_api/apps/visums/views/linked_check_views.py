import logging

from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.visums.models import LinkedCheck
from apps.visums.serializers import LinkedCheckSerializer


logger = logging.getLogger(__name__)


class LinkedCheckViewSet(viewsets.GenericViewSet):
    """
    A viewset for LinkedCheck instances.
    """

    serializer_class = LinkedCheckSerializer
    queryset = LinkedCheck.objects.all()
    filter_backends = [filters.DjangoFilterBackend]

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCheckSerializer})
    def retrieve(self, request, pk=None):
        instance: LinkedCheck = get_object_or_404(LinkedCheck.objects, pk=pk)
        serializer = LinkedCheckSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedCheckSerializer,
        responses={status.HTTP_200_OK: LinkedCheckSerializer},
    )
    def partial_update(self, request, pk=None):
        instance = self.get_object()

        logger.debug("LINKED CHECK UPDATE REQUEST DATA: %s", request.data)

        serializer = LinkedCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("LINKED CHECK UPDATE VALIDATED DATA: %s", validated_data)

        logger.debug("Updating LinkedCheck with id %s", pk)

        updated_instance = self.camp_visum_service.visum_update(
            request, instance=instance, **validated_data
        )

        output_serializer = LinkedCheckSerializer(
            updated_instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)
