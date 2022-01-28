import logging
from typing import List

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.participants.models import InuitsParticipant

from apps.visums.models import (
    CheckTypeEndpoint,
    LinkedCheck,
    LinkedSimpleCheck,
    LinkedDateCheck,
    LinkedDurationCheck,
    LinkedLocationCheck,
    LinkedParticipantCheck,
    LinkedFileUploadCheck,
    LinkedCommentCheck,
)
from apps.visums.serializers import (
    LinkedCheckSerializer,
    LinkedSimpleCheckSerializer,
    LinkedDateCheckSerializer,
    LinkedDurationCheckSerializer,
    LinkedLocationCheckSerializer,
    LinkedCampLocationCheckSerializer,
    LinkedParticipantCheckSerializer,
    LinkedFileUploadCheckSerializer,
    LinkedCommentCheckSerializer,
)
from apps.visums.services import LinkedCheckService

from scouts_auth.inuits.serializers import PersistedFileSerializer


logger = logging.getLogger(__name__)


class LinkedCheckViewSet(viewsets.GenericViewSet):
    """
    A viewset for LinkedCheck instances.
    """

    serializer_class = LinkedCheckSerializer
    queryset = LinkedCheck.objects.all()
    filter_backends = [filters.DjangoFilterBackend]

    linked_check_service = LinkedCheckService()

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCheckSerializer})
    def retrieve(self, request, pk=None):
        instance: LinkedCheck = get_object_or_404(LinkedCheck.objects, pk=pk)
        serializer = LinkedCheckSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCheckSerializer})
    def list(self, request):
        """
        Gets all Check instances (filtered).
        """

        return self._list(instances=self.filter_queryset(self.get_queryset()))

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCheckSerializer})
    def retrieve_simple_check(self, request, check_id=None):
        instance: LinkedCheck = self.linked_check_service.get_simple_check(check_id)
        serializer = LinkedCheckSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedSimpleCheckSerializer,
        responses={status.HTTP_200_OK: LinkedSimpleCheckSerializer},
    )
    def partial_update_simple_check(self, request, check_id):
        logger.debug("SIMPLE CHECK UPDATE REQUEST DATA: %s", request.data)
        instance: LinkedSimpleCheck = self.linked_check_service.get_simple_check(
            check_id
        )

        serializer = LinkedSimpleCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("SIMPLE CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_simple_check(
            instance, **validated_data
        )

        output_serializer = LinkedSimpleCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"simple",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedSimpleCheckSerializer})
    def list_simple_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.SIMPLE_CHECK
            )
        )

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedDateCheckSerializer})
    def retrieve_data_check(self, request, check_id=None):
        instance: LinkedDateCheck = self.linked_check_service.get_date_check(check_id)
        serializer = LinkedDateCheckSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedDateCheckSerializer,
        responses={status.HTTP_200_OK: LinkedDateCheckSerializer},
    )
    def partial_update_date_check(self, request, check_id):
        logger.debug("DATE CHECK UPDATE REQUEST DATA: %s", request.data)
        instance = self.linked_check_service.get_date_check(check_id)

        serializer = LinkedDateCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("DATE CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_date_check(
            instance, **validated_data
        )

        output_serializer = LinkedDateCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"date",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedDateCheckSerializer})
    def list_date_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.DATE_CHECK
            )
        )

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedDurationCheckSerializer})
    def retrieve_duration_check(self, request, check_id=None):
        instance: LinkedDurationCheck = self.linked_check_service.get_duration_check(
            check_id
        )
        serializer = LinkedDurationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedDurationCheckSerializer,
        responses={status.HTTP_200_OK: LinkedDurationCheckSerializer},
    )
    def partial_update_duration_check(self, request, check_id):
        logger.debug("DURATION CHECK UPDATE REQUEST DATA: %s", request.data)
        instance = self.linked_check_service.get_duration_check(check_id)

        serializer = LinkedDurationCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("DURATION CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_duration_check(
            instance, **validated_data
        )

        output_serializer = LinkedDurationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"duration",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedDurationCheckSerializer})
    def list_duration_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.DURATION_CHECK
            )
        )

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedLocationCheckSerializer})
    def retrieve_location_check(self, request, check_id=None):
        instance: LinkedLocationCheck = self.linked_check_service.get_location_check(
            check_id
        )
        serializer = LinkedLocationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedLocationCheckSerializer,
        responses={status.HTTP_200_OK: LinkedLocationCheckSerializer},
    )
    def partial_update_location_check(self, request, check_id):
        logger.debug("LOCATION CHECK UPDATE REQUEST DATA: %s", request.data)
        instance = self.linked_check_service.get_location_check(check_id)

        serializer = LinkedLocationCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("LOCATION CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_location_check(
            instance, **validated_data
        )

        output_serializer = LinkedLocationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"location",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedLocationCheckSerializer})
    def list_location_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.LOCATION_CHECK
            )
        )

    @action(
        detail=False,
        methods=["get"],
        url_path=r"location/linked",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedLocationCheckSerializer})
    def list_linked_location_checks(self, request):
        return self._list(
            LinkedLocationCheck.objects.filter(
                Q(parent__check_type__check_type=CheckTypeEndpoint.LOCATION_CHECK)
                & Q(locations__isnull=False)
            )
        )

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedCampLocationCheckSerializer}
    )
    def retrieve_camp_location_check(self, request, check_id=None):
        instance: LinkedLocationCheck = (
            self.linked_check_service.get_camp_location_check(check_id)
        )
        serializer = LinkedCampLocationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedCampLocationCheckSerializer,
        responses={status.HTTP_200_OK: LinkedCampLocationCheckSerializer},
    )
    def partial_update_camp_location_check(self, request, check_id):
        logger.debug("CAMP LOCATION CHECK UPDATE REQUEST DATA: %s", request.data)
        instance = self.linked_check_service.get_camp_location_check(check_id)

        serializer = LinkedCampLocationCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CAMP LOCATION CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_camp_location_check(
            instance, **validated_data
        )

        output_serializer = LinkedCampLocationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"camp_location",
    )
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedCampLocationCheckSerializer}
    )
    def list_camp_location_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.CAMP_LOCATION_CHECK
            )
        )

    @action(
        detail=False,
        methods=["get"],
        url_path=r"camp_location/linked",
    )
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedCampLocationCheckSerializer}
    )
    def list_linked_camp_location_checks(self, request):
        return self._list(
            LinkedLocationCheck.objects.filter(
                Q(is_camp_location=False)
                & Q(
                    parent__check_type__check_type=CheckTypeEndpoint.CAMP_LOCATION_CHECK
                )
                & Q(locations__isnull=False)
            )
        )

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedParticipantCheckSerializer}
    )
    def retrieve_participant_check(self, request, check_id=None):
        instance: LinkedParticipantCheck = (
            self.linked_check_service.get_participant_check(check_id)
        )
        serializer = LinkedParticipantCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedParticipantCheckSerializer,
        responses={status.HTTP_200_OK: LinkedParticipantCheckSerializer},
    )
    def partial_update_participant_check(self, request, check_id):
        logger.debug("PARTICIPANT CHECK UPDATE REQUEST DATA: %s", request.data)
        instance = self.linked_check_service.get_participant_check(check_id)

        serializer = LinkedParticipantCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("PARTICIPANT CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_participant_check(
            request, instance, **validated_data
        )

        output_serializer = LinkedParticipantCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LinkedParticipantCheckSerializer,
        responses={status.HTTP_200_OK: LinkedParticipantCheckSerializer},
    )
    def unlink_participant(self, request, check_id, participant_id):
        logger.debug("PARTICIPANT CHECK UNLINK REQUEST DATA: %s", request.data)
        instance = self.linked_check_service.get_participant_check(check_id)

        if not instance:
            logger.error(
                "Can't unlink participant: Unknown participant check with id {}".format(
                    check_id
                )
            )
            raise Http404

        serializer = LinkedParticipantCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("PARTICIPANT CHECK UNLINK VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.unlink_participant(
            request, instance, participant_id, **validated_data
        )

        output_serializer = LinkedParticipantCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"participant",
    )
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedParticipantCheckSerializer}
    )
    def list_participant_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.PARTICIPANT_CHECK
            )
        )

    @action(
        detail=False,
        methods=["get"],
        url_path=r"participant/linked",
    )
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedParticipantCheckSerializer}
    )
    def list_linked_participant_checks(self, request):
        return self._list(
            LinkedParticipantCheck.objects.filter(
                Q(parent__check_type__check_type=CheckTypeEndpoint.PARTICIPANT_CHECK)
                & Q(value__isnull=False)
            ).distinct()
        )

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedFileUploadCheckSerializer}
    )
    def retrieve_file_upload_check(self, request, check_id=None):
        instance: LinkedFileUploadCheck = (
            self.linked_check_service.get_file_upload_check(check_id)
        )
        serializer = LinkedFileUploadCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedFileUploadCheckSerializer,
        responses={status.HTTP_200_OK: LinkedFileUploadCheckSerializer},
    )
    def partial_update_file_upload_check(self, request, check_id):
        logger.debug("FILE UPLOAD CHECK UPDATE REQUEST DATA: %s", request.data)
        instance: LinkedFileUploadCheck = (
            self.linked_check_service.get_file_upload_check(check_id)
        )

        serializer = PersistedFileSerializer(
            data=request.data, context={"request": request}
        )
        # serializer = LinkedFileUploadCheckSerializer(
        #     data=request.data,
        #     instance=instance,
        #     context={"request": request},
        #     partial=True,
        # )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("FILE UPLOAD CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_file_upload_check(
            instance=instance, uploaded_file=validated_data.get("file")
        )

        output_serializer = LinkedFileUploadCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LinkedFileUploadCheckSerializer,
        responses={status.HTTP_200_OK: LinkedFileUploadCheckSerializer},
    )
    def unlink_file(self, request, check_id):
        logger.debug("FILE UPLOAD CHECK UNLINK REQUEST DATA: %s", request.data)
        instance = self.linked_check_service.get_file_upload_check(check_id)

        if not instance:
            logger.error(
                "Can't unlink file: Unknown file check with id {}".format(check_id)
            )
            raise Http404

        serializer = LinkedFileUploadCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("FILE UPLOAD CHECK UNLINK VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.unlink_file(
            request, instance, **validated_data
        )

        output_serializer = LinkedFileUploadCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"file",
    )
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedFileUploadCheckSerializer}
    )
    def list_file_upload_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.FILE_UPLOAD_CHECK
            )
        )

    @action(
        detail=False,
        methods=["get"],
        url_path=r"file/linked",
    )
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedFileUploadCheckSerializer}
    )
    def list_linked_files(self, request):
        return self._list(
            LinkedFileUploadCheck.objects.filter(
                Q(parent__check_type__check_type=CheckTypeEndpoint.FILE_UPLOAD_CHECK)
                & Q(value__isnull=False)
            )
        )

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCommentCheckSerializer})
    def retrieve_comment_check(self, request, check_id=None):
        instance: LinkedCommentCheck = self.linked_check_service.get_comment_check(
            check_id
        )
        serializer = LinkedCommentCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedCommentCheckSerializer,
        responses={status.HTTP_200_OK: LinkedCommentCheckSerializer},
    )
    def partial_update_comment_check(self, request, check_id):
        logger.debug("COMMENT CHECK UPDATE REQUEST DATA: %s", request.data)
        instance = self.linked_check_service.get_comment_check(check_id)

        serializer = LinkedCommentCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("COMMENT CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_comment_check(
            instance, **validated_data
        )

        output_serializer = LinkedCommentCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"comment",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCommentCheckSerializer})
    def list_comment_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.COMMENT_CHECK
            )
        )

    def _list(self, instances: List[LinkedCheck]):
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = LinkedCheckSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = LinkedCheckSerializer(instances, many=True)
            return Response(serializer.data)
