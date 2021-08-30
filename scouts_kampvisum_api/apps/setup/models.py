import logging

from rest_framework import serializers


logger = logging.getLogger(__name__)


class SetupItem:

    name = ''
    ok = False
    endpoint = ''
    # Action to perform
    module = None
    function = None
    args = None

    creation_count = 0
    objects = ()

    def __init__(self,
                 name, ok=False, endpoint='', module=None,
                 function=None, args=None) -> None:
        self.name = name
        self.ok = ok
        self.endpoint = endpoint
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
        return len(self.objects)

    def check(self):
        if self.args is not None:
            getattr(globals()[self.module](), self.function)(*self.args)
        else:
            getattr(globals()[self.module](), self.function)()


class Setup:

    global_status = False
    endpoint = '/api/setup/init'
    items = []

    def perform_init(self, request):
        status = True

        self.items = [
            SetupItem('years',
                      module="CampYearService",
                      function="setup_camp_years",
                      args=None),
            SetupItem('groups',
                      endpoint='/api/groups/import',
                      module="GroupService",
                      function="import_ga_groups",
                      args=[request.user]),
            SetupItem('sections',
                      module="GroupService",
                      function="link_default_sections",
                      args=None),
            SetupItem('category_sets',
                      endpoint='/api/category_sets/import',
                      module="CampVisumCategorySetService",
                      function="setup_default",
                      args=None),
        ]

        for item in self.items:
            logger.info("Performing setup for action '%s'", item.name)
            item.check()
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
    endpoint = serializers.CharField(default='')


class SetupSerializer(serializers.Serializer):
    """
    Serializes setup information.
    """

    global_status = serializers.BooleanField(default=False)
    endpoint = serializers.CharField(default='')
    items = SetupItemSerializer(many=True)
