from typing import List

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied

from apps.visums.models import (
    LinkedCheck,
    LinkedSimpleCheck,
    LinkedDateCheck,
    LinkedDurationCheck,
    LinkedLocationCheck,
    LinkedParticipantCheck,
    LinkedFileUploadCheck,
    LinkedCommentCheck,
    LinkedNumberCheck,
)
from apps.visums.models.enums import CheckTypeEnum
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
    LinkedNumberCheckSerializer,
)
from apps.visums.services import LinkedCheckService
from apps.visums.utils import CheckValidator
from scouts_auth.groupadmin.services import ScoutsAuthorizationService

from scouts_auth.inuits.models import PersistedFile
from scouts_auth.inuits.serializers import PersistedFileSerializer
from scouts_auth.groupadmin.models import ScoutsGroup, ScoutsFunction 

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedCheckViewSet(viewsets.GenericViewSet):
    """
    A viewset for LinkedCheck instances.
    """

    serializer_class = LinkedCheckSerializer
    queryset = LinkedCheck.objects.all()
    filter_backends = [filters.DjangoFilterBackend]

    linked_check_service = LinkedCheckService()
    authorization_service = ScoutsAuthorizationService()

    def check_user_allowed(self, request, instance: LinkedCheck):
        group = instance.sub_category.category.category_set.visum.group
        # This should probably be handled by a rest call when changing groups in the frontend,
        # but adding it here avoids the need for changes to the frontend
        self.authorization_service.update_user_authorizations(
            user=request.user, scouts_group=group
        )

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
        self.check_user_allowed(request, instance)
        serializer = LinkedCheckSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedSimpleCheckSerializer,
        responses={status.HTTP_200_OK: LinkedSimpleCheckSerializer},
    )
    def partial_update_simple_check(self, request, check_id):
        # logger.debug("SIMPLE CHECK UPDATE REQUEST DATA: %s", request.data)
        instance: LinkedSimpleCheck = self.linked_check_service.get_simple_check(
            check_id
        )
        self.check_user_allowed(request, instance)

        serializer = LinkedSimpleCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        # logger.debug("SIMPLE CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_simple_check(
            request=request, instance=instance, **validated_data
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
                parent__check_type__check_type=CheckTypeEnum.SIMPLE_CHECK
            )
        )

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedDateCheckSerializer})
    def retrieve_data_check(self, request, check_id=None):
        instance: LinkedDateCheck = self.linked_check_service.get_date_check(check_id)
        self.check_user_allowed(request, instance)

        serializer = LinkedDateCheckSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedDateCheckSerializer,
        responses={status.HTTP_200_OK: LinkedDateCheckSerializer},
    )
    def partial_update_date_check(self, request, check_id):
        # logger.debug("DATE CHECK UPDATE REQUEST DATA: %s", request.data)
        instance = self.linked_check_service.get_date_check(check_id)
        self.check_user_allowed(request, instance)

        serializer = LinkedDateCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        # logger.debug("DATE CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_date_check(
            request=request, instance=instance, **validated_data
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
                parent__check_type__check_type=CheckTypeEnum.DATE_CHECK
            )
        )

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedDurationCheckSerializer})
    def retrieve_duration_check(self, request, check_id=None):
        instance: LinkedDurationCheck = self.linked_check_service.get_duration_check(
            check_id
        )
        self.check_user_allowed(request, instance)

        serializer = LinkedDurationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedDurationCheckSerializer,
        responses={status.HTTP_200_OK: LinkedDurationCheckSerializer},
    )
    def partial_update_duration_check(self, request, check_id):
        # logger.debug("DURATION CHECK UPDATE REQUEST DATA: %s", request.data)
        instance = self.linked_check_service.get_duration_check(check_id)
        self.check_user_allowed(request, instance)

        serializer = LinkedDurationCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        # logger.debug("DURATION CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_duration_check(
            request=request, instance=instance, **validated_data
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
                parent__check_type__check_type=CheckTypeEnum.DURATION_CHECK
            )
        )

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedLocationCheckSerializer})
    def retrieve_location_check(self, request, check_id=None):
        instance: LinkedLocationCheck = self.linked_check_service.get_location_check(
            check_id
        )
        self.check_user_allowed(request, instance)

        serializer = LinkedLocationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedLocationCheckSerializer,
        responses={status.HTTP_200_OK: LinkedLocationCheckSerializer},
    )
    def partial_update_location_check(self, request, check_id):
        # logger.debug("LOCATION CHECK UPDATE REQUEST DATA: %s", request.data)
        instance = self.linked_check_service.get_location_check(check_id)
        self.check_user_allowed(request, instance)

        serializer = LinkedLocationCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        # logger.debug("LOCATION CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_location_check(
            request=request, instance=instance, **validated_data
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
                parent__check_type__check_type=CheckTypeEnum.LOCATION_CHECK
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
                Q(parent__check_type__check_type=CheckTypeEnum.LOCATION_CHECK)
                & Q(value__locations__isnull=False)
            )
        )

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedCampLocationCheckSerializer}
    )
    def retrieve_camp_location_check(self, request, check_id=None):
        instance: LinkedLocationCheck = (
            self.linked_check_service.get_camp_location_check(check_id)
        )
        self.check_user_allowed(request, instance)

        serializer = LinkedCampLocationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedCampLocationCheckSerializer,
        responses={status.HTTP_200_OK: LinkedCampLocationCheckSerializer},
    )
    def partial_update_camp_location_check(self, request, check_id):
        instance = self.linked_check_service.get_camp_location_check(check_id)
        self.check_user_allowed(request, instance)

        serializer = LinkedCampLocationCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        for location in validated_data["locations"]:
            if hasattr(location, 'checks'):
                for check in location.checks.all():
                    self.check_user_allowed(request, check)

        logger.debug("CAMP LOCATION CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_camp_location_check(
            request=request, instance=instance, **validated_data
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
                parent__check_type__check_type=CheckTypeEnum.CAMP_LOCATION_CHECK
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
                Q(value__is_camp_location=True)
                & Q(parent__check_type__check_type=CheckTypeEnum.CAMP_LOCATION_CHECK)
                & Q(value__locations__isnull=False)
            )
        )

    def _get_and_validate_participant_check(self, check_id=None):
        if not check_id:
            raise ValidationError(
                "Can't execute ParticipantCheck CRUD without a check id"
            )

        instance: LinkedParticipantCheck = (
            self.linked_check_service.get_participant_check(check_id)
        )

        if not instance:
            logger.error(
                "Can't unlink participant: Unknown participant check with id {}",
                check_id,
            )
            raise ValidationError(
                "Can't unlink participant: Unknown participant check with id {}".format(
                    check_id
                )
            )

        return instance

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedParticipantCheckSerializer}
    )
    def retrieve_participant_check(self, request, check_id=None):
        instance: LinkedParticipantCheck = self._get_and_validate_participant_check(
            check_id=check_id
        )
        self.check_user_allowed(request, instance)

        serializer = LinkedParticipantCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedParticipantCheckSerializer,
        responses={status.HTTP_200_OK: LinkedParticipantCheckSerializer},
    )
    def partial_update_participant_check(self, request, check_id):
        # logger.debug("PARTICIPANT CHECK UPDATE REQUEST DATA: %s", request.data)
        instance: LinkedParticipantCheck = self._get_and_validate_participant_check(
            check_id=check_id
        )
        self.check_user_allowed(request, instance)

        serializer = LinkedParticipantCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("PARTICIPANT CHECK UPDATE VALIDATED DATA: %s", validated_data)

        if instance.parent.validators:
            if not CheckValidator.validate(instance.parent.validators, instance, group_admin_id=validated_data.get("participants", [])[0].get("participant", None).group_admin_id):
                raise ValidationError(f"LinkedParticipantCheck is not valid: {instance}")
        
        instance = self.linked_check_service.update_participant_check(
            request=request, instance=instance, **validated_data
        )

        output_serializer = LinkedParticipantCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LinkedParticipantCheckSerializer,
        responses={status.HTTP_200_OK: LinkedParticipantCheckSerializer},
    )
    def toggle_participant_payment_status(
        self, request, check_id, visum_participant_id
    ):
        instance: LinkedParticipantCheck = self._get_and_validate_participant_check(
            check_id=check_id
        )
        self.check_user_allowed(request, instance)

        instance = self.linked_check_service.toggle_participant_payment_status(
            request=request,
            instance=instance,
            visum_participant_id=visum_participant_id,
        )

        output_serializer = LinkedParticipantCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LinkedParticipantCheckSerializer,
        responses={status.HTTP_200_OK: LinkedParticipantCheckSerializer},
    )
    def unlink_participant(self, request, check_id, visum_participant_id):
        # logger.debug("PARTICIPANT CHECK UNLINK REQUEST DATA: %s", request.data)
        instance: LinkedParticipantCheck = self._get_and_validate_participant_check(
            check_id=check_id
        )
        self.check_user_allowed(request, instance)

        serializer = LinkedParticipantCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        # logger.debug("PARTICIPANT CHECK UNLINK VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.unlink_participant(
            request=request,
            instance=instance,
            visum_participant_id=visum_participant_id,
            **validated_data
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
                Q(parent__check_type__check_type=CheckTypeEnum.PARTICIPANT_CHECK)
                | Q(
                    parent__check_type__check_type=CheckTypeEnum.PARTICIPANT_MEMBER_CHECK
                )
                | Q(parent__check_type__check_type=CheckTypeEnum.PARTICIPANT_COOK_CHECK)
                | Q(
                    parent__check_type__check_type=CheckTypeEnum.PARTICIPANT_LEADER_CHECK
                )
                | Q(
                    parent__check_type__check_type=CheckTypeEnum.PARTICIPANT_RESPONSIBLE_CHECK
                )
                | Q(
                    parent__check_type__check_type=CheckTypeEnum.PARTICIPANT_ADULT_CHECK
                )
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
                Q(parent__check_type__check_type=CheckTypeEnum.PARTICIPANT_CHECK)
                | Q(
                    parent__check_type__check_type=CheckTypeEnum.PARTICIPANT_MEMBER_CHECK
                )
                | Q(parent__check_type__check_type=CheckTypeEnum.PARTICIPANT_COOK_CHECK)
                | Q(
                    parent__check_type__check_type=CheckTypeEnum.PARTICIPANT_LEADER_CHECK
                )
                | Q(
                    parent__check_type__check_type=CheckTypeEnum.PARTICIPANT_RESPONSIBLE_CHECK
                )
                | Q(
                    parent__check_type__check_type=CheckTypeEnum.PARTICIPANT_ADULT_CHECK
                )
            )
            .filter(Q(participants__isnull=False))
            .distinct()
        )

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedFileUploadCheckSerializer}
    )
    def retrieve_file_upload_check(self, request, check_id=None):
        instance: LinkedFileUploadCheck = (
            self.linked_check_service.get_file_upload_check(check_id)
        )
        self.check_user_allowed(request, instance)

        serializer = LinkedFileUploadCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedFileUploadCheckSerializer,
        responses={status.HTTP_200_OK: LinkedFileUploadCheckSerializer},
    )
    def partial_update_file_upload_check(self, request, check_id):
        # logger.debug("FILE UPLOAD CHECK UPDATE REQUEST DATA: %s", request.data)
        instance: LinkedFileUploadCheck = (
            self.linked_check_service.get_file_upload_check(check_id)
        )
        self.check_user_allowed(request, instance)

        files = request.data.get("value", [])
        if not files or len(files) == 0:
            raise ValidationError("Can't link an empty list of files")

        serializer = PersistedFileSerializer(
            data=files, context={"request": request}, many=True
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        # logger.debug("FILE UPLOAD CHECK UPDATE VALIDATED DATA: %s", validated_data)

        for file in validated_data:
            for check in file.checks.all():
                self.check_user_allowed(request, check)
        
        instance = self.linked_check_service.update_file_upload_check(
            request=request, instance=instance, files=validated_data
        )

        output_serializer = LinkedFileUploadCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LinkedFileUploadCheckSerializer,
        responses={status.HTTP_200_OK: LinkedFileUploadCheckSerializer},
    )
    def unlink_file(self, request, check_id, persisted_file_id):
        # logger.debug("FILE UPLOAD CHECK UNLINK REQUEST DATA: %s", request.data)
        instance = self.linked_check_service.get_file_upload_check(check_id)
        self.check_user_allowed(request, instance)

        if not instance:
            logger.error("Can't unlink file: Unknown file check with id {}", check_id)
            raise ValidationError(
                "Can't unlink file: Unknown file check with id {}".format(check_id)
            )

        serializer = LinkedFileUploadCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        # logger.debug("FILE UPLOAD CHECK UNLINK VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.unlink_file(
            request=request,
            instance=instance,
            persisted_file_id=persisted_file_id,
            **validated_data
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
                parent__check_type__check_type=CheckTypeEnum.FILE_UPLOAD_CHECK
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
                Q(parent__check_type__check_type=CheckTypeEnum.FILE_UPLOAD_CHECK)
                & Q(value__isnull=False)
            ).distinct()
        )

    @action(
        detail=False,
        methods=["get"],
        url_path=r"file/search",
    )
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedFileUploadCheckSerializer}
    )
    def search_files(self, request):
        term = self.request.GET.get("term", None)
        group_admin_id = self.request.GET.get("group", None)
        if term and not group_admin_id:
            raise ValidationError(
                "Can only search for files if the group's group admin id is given"
            )

        if term:
            leader_functions: List[ScoutsFunction] = list(
                ScoutsFunction.objects.get_leader_functions(user=request.user)
            ) 

            group_admin_ids = []
            for leader_function in leader_functions:
                for group in leader_function.scouts_groups.all():
                    group_admin_ids.append(group.group_admin_id)

                    if request.user.has_role_district_commissioner():
                        underlyingGroups: List[ScoutsGroup] = list(
                            ScoutsGroup.objects.get_groups_with_parent(
                                parent_group_admin_id=group.group_admin_id
                            )
                        )

                        for underlyingGroup in underlyingGroups:
                            if leader_functions.is_district_commissioner_for_group(scouts_group=underlyingGroup):
                                group_admin_ids.append(underlyingGroup.group_admin_id)

            if not group_admin_id in group_admin_ids:
                raise PermissionDenied(
                    {
                        "message": "You don't have permission to request files for group {}".format(
                            group_admin_id
                        )
                    }
                )

            instances = (
                PersistedFile.objects.filter(
                    Q(
                        checks__parent__check_type__check_type=CheckTypeEnum.FILE_UPLOAD_CHECK
                    )
                    & Q(
                        checks__sub_category__category__category_set__visum__group__group_admin_id=group_admin_id
                    )
                )
                .distinct()
                .filter(Q(original_name__icontains=term))
            )

            page = self.paginate_queryset(instances)
            if page is not None:
                serializer = PersistedFileSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                serializer = PersistedFileSerializer(instances, many=True)
                return Response(serializer.data)

        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEnum.FILE_UPLOAD_CHECK
            )
        )

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCommentCheckSerializer})
    def retrieve_comment_check(self, request, check_id=None):
        instance: LinkedCommentCheck = self.linked_check_service.get_comment_check(
            check_id
        )
        self.check_user_allowed(request, instance)

        serializer = LinkedCommentCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedCommentCheckSerializer,
        responses={status.HTTP_200_OK: LinkedCommentCheckSerializer},
    )
    def partial_update_comment_check(self, request, check_id):
        # logger.debug("COMMENT CHECK UPDATE REQUEST DATA: %s", request.data)
        instance = self.linked_check_service.get_comment_check(check_id)
        self.check_user_allowed(request, instance)

        serializer = LinkedCommentCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        # logger.debug("COMMENT CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_comment_check(
            request=request, instance=instance, **validated_data
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
                parent__check_type__check_type=CheckTypeEnum.COMMENT_CHECK
            )
        )

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedNumberCheckSerializer})
    def retrieve_number_check(self, request, check_id=None):
        instance: LinkedNumberCheck = self.linked_check_service.get_number_check(
            check_id
        )
        self.check_user_allowed(request, instance)

        serializer = LinkedNumberCheckSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedNumberCheckSerializer,
        responses={status.HTTP_200_OK: LinkedNumberCheckSerializer},
    )
    def partial_update_number_check(self, request, check_id):
        # logger.debug("NUMBER CHECK UPDATE REQUEST DATA: %s", request.data)
        instance = self.linked_check_service.get_number_check(check_id)
        self.check_user_allowed(request, instance)

        serializer = LinkedNumberCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        # logger.debug("NUMBER CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_number_check(
            request=request, instance=instance, **validated_data
        )

        output_serializer = LinkedNumberCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"number",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedNumberCheckSerializer})
    def list_number_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEnum.NUMBER_CHECK
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
