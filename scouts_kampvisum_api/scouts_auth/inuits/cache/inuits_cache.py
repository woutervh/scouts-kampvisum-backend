import io
from typing import List

from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# from django.core.cache import cache

# from django_redis import get_redis_connection

from redis import Redis

from scouts_auth.groupadmin.models import (
    ScoutsUser,
    AbstractScoutsGroup,
    AbstractScoutsFunction,
)
from scouts_auth.groupadmin.serializers import (
    ScoutsUserSerializer,
    AbstractScoutsGroupSerializer,
    AbstractScoutsFunctionSerializer,
)

from scouts_auth.inuits.utils import Singleton


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


# @Singleton
class InuitsCache(metaclass=Singleton):

    redis = Redis(host="redis", port=6379)

    def __init__(self):
        logger.debug("CREATED InuitsCache")

    def store(self, key: str, data: str, clean: bool = True):
        if clean:
            self.redis.set(key, "")
        self.redis.set(key, data)

    def retrieve(self, key: str) -> str:
        return self.redis.get(key)

    def store_user_data(self, user: settings.AUTH_USER_MODEL):
        # https://www.thebookofjoel.com/redis-docker-compose-django
        # https://stackabuse.com/working-with-redis-in-python-with-django/
        # logger.debug("REDIS URL: %s", settings.REDIS_URL)
        # get_redis_connection("default").set("test", "test")
        # cache.set(user.id, ScoutsUserSerializer(instance=user).data)
        # InuitsCache.instance.redis
        # logger.debug("GROUPS: %s", user.groups)
        # logger.debug("FUNCTIONS: %s", user.functions)

        group_data = AbstractScoutsGroupSerializer(user.scouts_groups, many=True).data
        function_data = AbstractScoutsFunctionSerializer(user.functions, many=True).data

        # logger.debug("CACHING GROUPS: %s", group_data)
        for function in function_data:
            logger.debug("CACHING FUNCTION: %s", function)

        # serialized = ScoutsUserSerializer(user).data
        # logger.debug(
        #     "SERIALIZED USER OBJECT: (%s) %s", type(serialized).__name__, serialized
        # )
        # rendered = JSONRenderer().render(serialized)
        # logger.debug("RENDERED USER OBJECT: (%s) %s", type(rendered).__name__, rendered)

        self.store(
            str(user.group_admin_id),
            JSONRenderer().render({"groups": group_data, "functions": function_data}),
        )

    def retrieve_user_data(self, user_id) -> settings.AUTH_USER_MODEL:
        # data = ScoutsUserSerializer(cache.get(user_id)).data
        # data = ScoutsUserSerializer(InuitsCache.instance.redis).data
        # data = self.redis.get(str(user_id))
        # logger.debug("RENDERED DATA: (%s) %s", type(data).__name__, data)

        # stream = io.BytesIO(data)
        # data = JSONParser().parse(stream)
        # logger.debug("PARSED DATA: (%s) %s", type(data).__name__, data)

        # serializer = ScoutsUserSerializer(data=data)
        # serializer.is_valid(raise_exception=True)

        # data = serializer.validated_data

        # logger.debug("Deserialized user data: %s", data)
        user: ScoutsUser = ScoutsUser.objects.get(id=user_id)

        data = JSONParser().parse(io.BytesIO(self.retrieve(str(user.group_admin_id))))
        group_data = data.get("groups", {})
        function_data = data.get("functions", {})

        # groups: List[AbstractScoutsGroup] = []
        for group in group_data:
            user.scouts_groups.append(
                AbstractScoutsGroupSerializer().create(validated_data=group)
            )
        # user.groups = groups
        # logger.debug("GROUPS: %s", user.scouts_groups)

        # functions: List[AbstractScoutsFunction] = []
        for function in function_data:
            user.functions.append(
                AbstractScoutsFunctionSerializer().create(validated_data=function)
            )
        # user.functions = functions
        logger.debug("FUNCTIONS: %s", user.functions)

        return user
