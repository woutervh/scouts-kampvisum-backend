from django.http.response import HttpResponse
from django_filters import rest_framework as filters
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from apps.visums.models import CampVisum
from apps.visums.serializers import CampVisumSerializer, CampVisumOverviewSerializer
from apps.visums.filters import CampVisumFilter
from apps.visums.services import CampVisumService

from scouts_auth.auth.permissions import CustomDjangoPermission

from scouts_auth.groupadmin.models import ScoutsGroup
from scouts_auth.scouts.permissions import ScoutsFunctionPermissions

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing camp instances.
    """

    serializer_class = CampVisumSerializer
    queryset = CampVisum.objects.all()
    permission_classes = (ScoutsFunctionPermissions,)
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CampVisumFilter

    camp_visum_service = CampVisumService()

    def has_group_admin_id(self) -> bool:
        return True

    def get_object(self, pk) -> CampVisum:
        return CampVisum.objects.safe_get(pk=pk, raise_error=True)

    @swagger_auto_schema(
        request_body=CampVisumSerializer,
        responses={status.HTTP_201_CREATED: CampVisumSerializer},
    )
    def create(self, request):
        data = request.data

        logger.debug("CAMP VISUM CREATE REQUEST DATA: %s", data)
        serializer = CampVisumSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CAMP VISUM CREATE VALIDATED DATA: %s", validated_data)

        visum: CampVisum = self.camp_visum_service.visum_create(
            request, **validated_data
        )

        output_serializer = CampVisumSerializer(visum, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampVisumSerializer})
    def retrieve(self, request, pk=None):
        logger.debug(f"Requesting visum {pk}", user=request.user)
        instance = self.get_object(pk=pk)
        logger.debug(f"Visum retrieved: {instance.name}")
        serializer = CampVisumSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CampVisumSerializer,
        responses={status.HTTP_200_OK: CampVisumSerializer},
    )
    def partial_update(self, request, pk=None):
        instance = self.get_object(pk=pk)

        logger.debug("CAMP VISUM UPDATE REQUEST DATA: %s", request.data)

        serializer = CampVisumSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CAMP VISUM UPDATE VALIDATED DATA: %s", validated_data)

        logger.debug("Updating CampVisum with id %s", pk)

        updated_instance = self.camp_visum_service.visum_update(
            request, instance=instance, **validated_data
        )

        output_serializer = CampVisumSerializer(
            updated_instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampVisumSerializer})
    def list(self, request):
        group_admin_id = self.request.query_params.get("group", None)
        year = self.request.query_params.get("year", None)
        logger.debug("Listing visums for group %s", group_admin_id, user=request.user)

        return self._list_response(
            request=request,
            instances=CampVisum.objects.get_all_for_group_and_year(
                group_admin_id=group_admin_id, year_number=year
            ),
        )

    def list_all(self, request):
        if not (
            request.user.has_role_administrator()
            or request.user.has_role_district_commissioner(ignore_group=True)
            or request.user.has_role_shire_president(ignore_group=True)
        ):
            raise PermissionDenied(
                f"[{request.user.username}] You are not allowed to list all visums"
            )

        if request.user.has_role_administrator():
            scouts_group_admin_ids = (
                CampVisum.objects.get_queryset().get_linked_groups()
            )
        elif request.user.has_role_shire_president(ignore_group=True):
            scouts_group_admin_ids = request.user.get_scouts_shire_president_groups()
        elif request.user.has_role_district_commissioner(ignore_group=True):
            scouts_group_admin_ids = (
                request.user.get_scouts_district_commissioner_groups()
            )

        return self._list_response(
            request=request,
            instances=CampVisum.objects.get_all_for_groups_and_year(
                request=request,
                group_admin_ids=scouts_group_admin_ids,
                year=request.GET.get("year", None),
            ),
            list_dc_overview=True,
        )

    def _list_response(self, request, instances, list_dc_overview: bool = False):
        page = self.paginate_queryset(instances)

        serializer = (
            CampVisumOverviewSerializer(
                page,
                many=True,
                context={"request": request, "list_dc_overview": list_dc_overview},
            )
            if page is not None
            else CampVisumOverviewSerializer(
                instances,
                list_dc_overview,
                many=True,
                context={"request": request, "list_dc_overview": list_dc_overview},
            )
        )
        response = serializer.data

        response.sort(
            key=lambda k: (
                k.get("group"),
                (
                    k.get("sections", [{"age_group": 0}])[0].get("age_group", 0)
                    if len(k.get("sections", [{"age_group": 0}])) > 0
                    else 0,
                ),
            )
        )

        if list_dc_overview:
            visums = []
            group_labels = []
            group_visums = []
            for visum in response:
                group_label = visum.get("group") + " " + visum.get("group_name")
                if group_label not in group_labels:
                    if group_labels:
                        last_group = group_labels.pop()
                        visums.append({"group": last_group, "camps": group_visums})
                        group_visums = []
                    group_labels.append(group_label)
                    group_visums.append(visum)
                else:
                    group_visums.append(visum)
            visums.append({"group": group_labels.pop(), "camps": group_visums})

            ## Another posibility to get visums for response, but with visums[-1] = it should works too because the response is sorted before
            # visums = []
            # group_labels = []
            # for visum in response:
            #     group_label = visum.get("group") + " " + visum.get("group_name")
            #     if group_label not in group_labels:
            #         group_labels.append(group_label)
            #         visums.append({"group": group_label, "camps": [visum]})
            #     else:
            #         visums[-1]["camps"].append(visum)

            response = visums

        return (
            self.get_paginated_response(response)
            if page is not None
            else Response(response)
        )

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def destroy(self, request, pk):
        instance = CampVisum.objects.safe_get(id=pk)

        self.camp_visum_service.delete_visum(request=request, instance=instance)

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampVisumSerializer})
    def dates_leaders(self, request, pk=None):
        logger.debug(f"Requesting camp dates for visum {pk}", user=request.user)

        return Response(CampVisum.objects.get_camp_dates(pk=pk))
