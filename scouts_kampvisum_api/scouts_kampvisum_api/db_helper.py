import logging, uuid

from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.groups.models import (
    ScoutsSectionName,
    ScoutsGroupType,
    DefaultScoutsSectionName,
)
from apps.visums.models import (
    CampYearCategorySet,
    CategorySetPriority,
    CategorySet,
    Category,
    SubCategory,
    CheckType,
    Check,
)


logger = logging.getLogger(__name__)


class DatabaseHelper:
    @staticmethod
    @receiver(pre_save)
    def set_uuid_on_save(sender, instance, *args, **kwargs):
        if instance.pk is None:
            logger.debug(
                "Generating UUID for %s fixture (sender: %s)",
                type(instance).__name__,
                sender,
                type(instance).__name__,
            )

            if isinstance(instance, DefaultScoutsSectionName):
                return DatabaseHelper.find_default_scouts_section_name(
                    instance, **kwargs
                )
            elif isinstance(instance, ScoutsGroupType):
                return DatabaseHelper.find_scouts_group_type(instance, **kwargs)
            elif isinstance(instance, ScoutsSectionName):
                return DatabaseHelper.find_scouts_section_name(instance, **kwargs)
            elif isinstance(instance, CampYearCategorySet):
                return DatabaseHelper.find_camp_year_category_set(instance, **kwargs)
            elif isinstance(instance, CategorySetPriority):
                return DatabaseHelper.find_category_set_priority(instance, **kwargs)
            elif isinstance(instance, CategorySet):
                return DatabaseHelper.find_category_set(instance, **kwargs)
            elif isinstance(instance, Category):
                return DatabaseHelper.find_category(instance, **kwargs)
            elif isinstance(instance, SubCategory):
                return DatabaseHelper.find_sub_category(instance, **kwargs)
            elif isinstance(instance, CheckType):
                return DatabaseHelper.find_check_type(instance, **kwargs)
            elif isinstance(instance, Check):
                return DatabaseHelper.find_check(instance, **kwargs)
            else:
                return

    @staticmethod
    def find_default_scouts_section_name(instance: DefaultScoutsSectionName, **kwargs):
        logger.debug("Finding INSTANCE %s: %s", type(instance).__name__, instance)
        try:
            instance = (
                DefaultScoutsSectionName.objects.all()
                .filter(type=kwargs.get("type"), name=kwargs.get("name"))
                .last()
            )
            if instance:
                logger.debug("Found INSTANCE %s: %s", type(instance).__name__, instance)
                return instance
            raise
        except:
            instance.id = uuid.uuid4()
            return instance

    @staticmethod
    def find_scouts_group_type(instance: ScoutsGroupType, **kwargs):
        logger.debug("Finding INSTANCE %s: %s", type(instance).__name__, instance)
        try:
            instance = (
                ScoutsGroupType.objects.all()
                .filter(group_type=kwargs.get("group_type"))
                .last()
            )
            if instance:
                logger.debug("Found INSTANCE %s: %s", type(instance).__name__, instance)
                return instance
            raise
        except:
            instance.id = uuid.uuid4()
            return instance

    @staticmethod
    def find_scouts_section_name(instance: ScoutsSectionName, **kwargs):
        logger.debug("Finding INSTANCE %s: %s", type(instance).__name__, instance)
        try:
            instance = (
                ScoutsSectionName.objects.all()
                .filter(
                    name=kwargs.get("name"),
                    gender=kwargs.get("gender"),
                    age_group=kwargs.get("age_group"),
                )
                .last()
            )
            if instance:
                logger.debug("Found INSTANCE %s: %s", type(instance).__name__, instance)
                return instance
            raise
        except:
            instance.id = uuid.uuid4()
            return instance

    @staticmethod
    def find_camp_year_category_set(instance: CampYearCategorySet, **kwargs):
        logger.debug("Finding INSTANCE %s: %s", type(instance).__name__, instance)
        try:
            instance = (
                CampYearCategorySet.objects.all()
                .filter(camp_year__year=kwargs.get("camp_year"))
                .last()
            )
            if instance:
                logger.debug("Found INSTANCE %s: %s", type(instance).__name__, instance)
                return instance
            raise
        except:
            instance.id = uuid.uuid4()
            return instance

    @staticmethod
    def find_category_set_priority(instance: CategorySetPriority, **kwargs):
        logger.debug("Finding INSTANCE %s: %s", type(instance).__name__, instance)
        try:
            instance = (
                CategorySetPriority.objects.all()
                .filter(owner=kwargs.get("owner"))
                .last()
            )
            if instance:
                logger.debug("Found INSTANCE %s: %s", type(instance).__name__, instance)
                return instance
            raise
        except:
            instance.id = uuid.uuid4()
            return instance

    @staticmethod
    def find_category_set(instance: CategorySet, **kwargs):
        logger.debug("Finding INSTANCE %s: %s", type(instance).__name__, instance)
        try:
            instance = (
                CategorySet.objects.all()
                .filter(
                    category_set__camp_year__year=kwargs.get("category_set")
                )
                .last()
            )
            if instance:
                logger.debug("Found INSTANCE %s: %s", type(instance).__name__, instance)
                return instance
            raise
        except:
            instance.id = uuid.uuid4()
            return instance

    @staticmethod
    def find_category(instance: Category, **kwargs):
        logger.debug("Finding INSTANCE %s: %s", type(instance).__name__, instance)
        try:
            instance = (
                Category.objects.all()
                .filter(
                    name=kwargs.get("name"), category_set=kwargs.get("category_set")
                )
                .last()
            )
            if instance:
                logger.debug("Found INSTANCE %s: %s", type(instance).__name__, instance)
                return instance
            raise
        except:
            instance.id = uuid.uuid4()
            return instance

    @staticmethod
    def find_sub_category(instance: SubCategory, **kwargs):
        logger.debug("Finding INSTANCE %s: %s", type(instance).__name__, instance)
        try:
            instance = (
                SubCategory.objects.all()
                .filter(name=kwargs.get("name"), category_set=kwargs.get())
                .last()
            )
            if instance:
                logger.debug("Found INSTANCE %s: %s", type(instance).__name__, instance)
                return instance
            raise
        except:
            instance.id = uuid.uuid4()
            return instance

    @staticmethod
    def find_check_type(instance: CheckType, **kwargs):
        logger.debug("Finding INSTANCE %s: %s", type(instance).__name__, instance)
        try:
            instance = (
                CheckType.objects.all().filter(check_type=kwargs.get("type")).last()
            )
            if instance:
                logger.debug("Found INSTANCE %s: %s", type(instance).__name__, instance)
                return instance
            raise
        except:
            instance.id = uuid.uuid4()
            return instance

    @staticmethod
    def find_check(instance: Check, **kwargs):
        logger.debug("Finding INSTANCE %s: %s", type(instance).__name__, instance)
        try:
            instance = Check.objects.all().filter(type=kwargs.get("type")).last()
            if instance:
                logger.debug("Found INSTANCE %s: %s", type(instance).__name__, instance)
                return instance
            raise
        except:
            instance.id = uuid.uuid4()
            return instance
