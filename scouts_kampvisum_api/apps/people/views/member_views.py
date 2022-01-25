import logging
from typing import List

from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.people.models import InuitsMember
from apps.people.serializers import InuitsMemberSerializer
from apps.people.filters import InuitsMemberFilter

from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.serializers import AbstractScoutsMemberSerializer
from scouts_auth.groupadmin.services import GroupAdminMemberService


logger = logging.getLogger(__name__)


class MemberViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsMemberFilter
    ordering_fields = ["id"]
    ordering = ["id"]
    queryset = InuitsMember.objects.all()

    service = GroupAdminMemberService()
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsMemberSerializer})
    def retrieve(self, request, pk):
        member: InuitsMember = None
        try:
            member = self.get(pk=pk)
        except:
            pass
        
        if not member:
            logger.debug("No member found with uuid %s", pk)
            scouts_member: AbstractScoutsMember = self.service.get_member_info(active_user=request.user, group_admin_id=pk)
            
            if not scouts_member:
                logger.debug("No scouts member found with group admin id %s", pk)
                return Response({})

            member = InuitsMember()
            
            member.group_admin_id = pk
            member.first_name = scouts_member.first_name
            member.last_name = scouts_member.last_name
            member.birth_date = scouts_member.birth_date
                
        serializer = InuitsMemberSerializer(member, context={"request": request})
        
        return Response(serializer.data)
            
    
    @action(
        detail=False,
        methods=["get"],
        url_path=r"ga/(?P<group_admin_id>\w+)",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: AbstractScoutsMemberSerializer})
    def retrieve_scouts_member(self, request, group_admin_id):
        logger.debug("Retrieving scouts member with group admin id %s", group_admin_id)
        member: AbstractScoutsMember = self.service.get_member_info(active_user=request.user, group_admin_id=group_admin_id)
        
        serializer = AbstractScoutsMemberSerializer(member, context={"request": request})
        
        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsMemberSerializer})
    def list(self, request):
        inuits_members = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(inuits_members)

        if page is not None:
            serializer = InuitsMemberSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InuitsMemberSerializer(inuits_members, many=True)
            return Response(serializer.data)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsMemberSerializer})
    def list_scouts_member(self, request, include_inactive: bool = False):
        search_term = self.request.GET.get("term", None)
        group_group_admin_id = self.request.GET.get("group", None)

        if not search_term:
            raise ValidationError("Url param 'term' is a required filter")

        if not group_group_admin_id:
            logger.debug(
                "Searching for members and non-members with search term %s", search_term
            )
        else:
            logger.debug(
                "Searching for members and non-members with term %s and group %s",
                search_term,
                group_group_admin_id,
            )

        members: List[AbstractScoutsMember] = self.service.search_member_filtered(
            active_user=request.user,
            term=search_term,
            group_group_admin_id=group_group_admin_id,
        )
        
        members: List[InuitsMember] = [InuitsMember(group_admin_id=member.group_admin_id, first_name=member.first_name, last_name=member.last_name, birth_date=member.birth_date) for member in members]

        output_serializer = InuitsMemberSerializer(members, many=True)

        return Response(output_serializer.data)
