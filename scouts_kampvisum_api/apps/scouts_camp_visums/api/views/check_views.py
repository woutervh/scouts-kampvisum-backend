import logging
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from ..models import ScoutsCampVisumCheck
#from ..services import ScoutsCampVisum
#from ..serializers import ScoutsCampVisumSubCategorySerializer


logger = logging.getLogger(__name__)


class ScoutsCampVisumCheckViewSet(viewsets.GenericViewSet):
    pass