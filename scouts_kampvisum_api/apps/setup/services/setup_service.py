import importlib

from rest_framework import serializers


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class SetupItem:

    name = ""
    ok = False
    endpoint = ""
    # Action to perform
    namespace = None
    module = None
    function = None
    args = None

    creation_count = 0
    objects = ()

    def __init__(
        self,
        name,
        ok=False,
        endpoint="",
        namespace=None,
        module=None,
        function=None,
        args=None,
    ) -> None:
        self.name = name
        self.ok = ok
        self.endpoint = endpoint
        self.namespace = namespace
        self.module = module
        self.function = function
        self.args = args

    def status(self):
        return self.ok

    def add_object(self, object):
        self.objects.push(object)

    def add_objects(self, objects):
        for object in objects:
            self.objects.push(object)

    def count_objects(self, objects):
        if self.creation_count is None:
            self.creation_count = len(self.objects)

        return self.creation_count

    def verify_setup(self):
        """Runs the setup action"""
        logger.debug("from %s import %s", self.namespace, self.module)
        mod = importlib.import_module(self.namespace)
        the_class = getattr(mod, self.module)()
        if self.args is not None:
            self.creation_count = len(getattr(the_class, self.function)(*self.args))
        else:
            self.creation_count = len(getattr(the_class, self.function)())


class Setup:

    global_status = False
    endpoint = "/api/setup/init"
    items = []

    def perform_init(self, request):
        status = True

        self.items = [
            SetupItem(
                "years",
                namespace="apps.camps.services",
                module="CampYearService",
                function="setup_camp_years",
                args=[request],
            ),
            SetupItem(
                "sections",
                namespace="apps.groups.services",
                module="ScoutsSectionService",
                function="setup_default_sections",
                args=[request],
            ),
        ]

        for item in self.items:
            logger.info("Performing setup for action '%s'", item.name)
            item.verify_setup()
            status = item.status()

            if not status:
                logger.error("Couldn't setup for item '%s'", item.name)

        self.global_status = status

        return self.global_status


class SetupItemSerializer(serializers.Serializer):
    """
    Serializes a setup item.
    """

    name = serializers.CharField()
    ok = serializers.BooleanField(default=False)
    creation_count = serializers.IntegerField(default=0)
    endpoint = serializers.CharField(default="")


class SetupSerializer(serializers.Serializer):
    """
    Serializes setup information.
    """

    global_status = serializers.BooleanField(default=False)
    endpoint = serializers.CharField(default="")
    items = SetupItemSerializer(many=True)
