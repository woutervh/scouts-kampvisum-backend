import logging
from typing import List

from django.http import Http404
from django.utils import timezone
from django.db import transaction

from apps.deadlines.models import (
    DefaultDeadline,
    DefaultDeadlineFlag,
    DefaultDeadlineSet,
    DeadlineDate,
    Deadline,
    DeadlineFlag,
    LinkedSubCategoryDeadline,
    LinkedCheckDeadline,
    MixedDeadline,
    DeadlineFactory,
)
from apps.deadlines.models.enums import DeadlineType
from apps.deadlines.services import DefaultDeadlineService

from apps.visums.models import (
    CampVisum,
    SubCategory,
    LinkedSubCategory,
    Check,
    LinkedCheck,
)


logger = logging.getLogger(__name__)


class DeadlineService:

    default_deadline_service = DefaultDeadlineService()

    @transaction.atomic
    def get_or_create_deadline(
        self,
        request,
        default_deadline: DefaultDeadline = None,
        visum: CampVisum = None,
        **fields
    ) -> Deadline:
        instance = Deadline.objects.safe_get(parent=default_deadline, visum=visum)
        if instance:
            return instance

        instance = Deadline()

        if default_deadline and isinstance(default_deadline, DefaultDeadline):
            instance.parent = default_deadline
        else:
            instance.parent = self.default_deadline_service.get_or_create(
                {
                    "name": fields.get("name", None),
                    "deadline_type": DeadlineType.DEADLINE,
                    "label": fields.get("label", None),
                    "description": fields.get("description", None),
                    "explanation": fields.get("explanation", None),
                    "is_important": fields.get("is_important", False),
                }
            )

        if visum and isinstance(visum, CampVisum):
            instance.visum = visum
        else:
            instance.visum = CampVisum.objects.safe_get(
                id=fields.get("visum", {}).get("id", None)
            )

        instance.created_by = request.user

        logger.debug(
            "Creating a %s instance for visum with id %s, with name %s and type %s",
            "Deadline",
            visum.id,
            instance.parent.name,
            instance.parent.deadline_type,
        )

        instance.full_clean()
        instance.save()

        if not (
            fields
            and isinstance(fields, dict)
            and "due_date" in fields
            and isinstance(fields.get("due_date"), dict)
        ):
            fields["due_date"] = dict()
        due_date: DeadlineDate = (
            self.default_deadline_service.get_or_create_deadline_date(
                default_deadline=instance.parent,
                **fields.get("due_date", None),
            )
        )

        return instance

    def get_deadline(self, deadline_id):
        try:
            return Deadline.objects.get(id=deadline_id)
        except Deadline.DoesNotExist:
            logger.error("Deadline with id %s not found", deadline_id)
            raise Http404

    def update_deadline(self, request, instance: Deadline, **fields):
        logger.debug(
            "Updating %s instance with id %s", type(instance).__name__, instance.id
        )

        instance.updated_by = request.user
        instance.updated_on = timezone.now()

        instance.full_clean()
        instance.save()

        if not (
            fields
            and isinstance(fields, dict)
            and "due_date" in fields
            and isinstance(fields.get("due_date"), dict)
        ):
            fields["due_date"] = dict()
        due_date: DeadlineDate = self.default_deadline_service.update_deadline_date(
            instance=instance.due_date, **fields.get("due_date", None)
        )

        return instance

    @transaction.atomic
    def get_or_create_linked_sub_category_deadline(
        self,
        request,
        default_deadline: DefaultDeadline = None,
        visum: CampVisum = None,
        **fields
    ) -> LinkedSubCategoryDeadline:
        instance = LinkedSubCategoryDeadline.objects.safe_get(
            parent=default_deadline, visum=visum
        )
        if instance:
            return instance

        # parent = self.get_or_create_deadline(
        #     request, default_deadline=default_deadline, visum=visum, **fields
        # )

        instance = LinkedSubCategoryDeadline()

        instance.parent = default_deadline
        instance.visum = visum

        logger.debug(
            "Creating a %s instance for visum with id %s, with name %s and type %s",
            "LinkedSubCategoryDeadline",
            visum.id,
            default_deadline.name,
            default_deadline.deadline_type,
        )

        instance.full_clean()
        instance.save()

        if not (
            fields
            and isinstance(fields, dict)
            and "due_date" in fields
            and isinstance(fields.get("due_date"), dict)
        ):
            fields["due_date"] = dict()
        due_date: DeadlineDate = (
            self.default_deadline_service.get_or_create_deadline_date(
                default_deadline=default_deadline, **fields.get("due_date", None)
            )
        )

        return instance

    def get_linked_sub_category_deadline(self, deadline_id):
        try:
            return LinkedSubCategoryDeadline.objects.get(deadline_ptr=deadline_id)
        except LinkedSubCategoryDeadline.DoesNotExist:
            raise Http404

    @transaction.atomic
    def get_or_create_linked_check_deadline(
        self,
        request,
        default_deadline: DefaultDeadline = None,
        visum: CampVisum = None,
        **fields
    ) -> LinkedCheckDeadline:

        instance = LinkedCheckDeadline.objects.safe_get(
            parent=default_deadline, visum=visum
        )
        if instance:
            return instance

        # parent = self.get_or_create_deadline(
        #     request, default_deadline=default_deadline, visum=visum, **fields
        # )
        # logger.debug("PARENT: %s", parent)

        instance = LinkedCheckDeadline()

        instance.parent = default_deadline
        instance.visum = visum

        logger.debug(
            "Creating a %s instance for visum with id %s, with name %s and type %s",
            "LinkedCheckDeadline",
            visum.id,
            default_deadline.name,
            default_deadline.deadline_type,
        )

        instance.full_clean()
        instance.save()

        if not (
            fields
            and isinstance(fields, dict)
            and "due_date" in fields
            and isinstance(fields.get("due_date"), dict)
        ):
            fields["due_date"] = dict()
        due_date: DeadlineDate = (
            self.default_deadline_service.get_or_create_deadline_date(
                default_deadline=default_deadline, **fields.get("due_date", None)
            )
        )

        return instance

    def get_linked_check_deadline(self, deadline_id):
        try:
            return LinkedCheckDeadline.objects.get(deadline_ptr=deadline_id)
        except LinkedCheckDeadline.DoesNotExist:
            raise Http404

    @transaction.atomic
    def get_or_create_mixed_deadline(
        self,
        request,
        default_deadline: DefaultDeadline = None,
        visum: CampVisum = None,
        **fields
    ) -> MixedDeadline:

        instance = MixedDeadline.objects.safe_get(parent=default_deadline, visum=visum)
        if instance:
            return instance

        # parent = self.get_or_create_deadline(
        #     request, default_deadline=default_deadline, visum=visum, **fields
        # )
        # logger.debug("PARENT: %s", parent)

        instance = MixedDeadline()

        instance.parent = default_deadline
        instance.visum = visum

        logger.debug(
            "Creating a %s instance for visum with id %s, with name %s and type %s",
            "MixedDeadline",
            visum.id,
            default_deadline.name,
            default_deadline.deadline_type,
        )

        instance.full_clean()
        instance.save()

        if not (
            fields
            and isinstance(fields, dict)
            and "due_date" in fields
            and isinstance(fields.get("due_date"), dict)
        ):
            fields["due_date"] = dict()
        due_date: DeadlineDate = (
            self.default_deadline_service.get_or_create_deadline_date(
                default_deadline=default_deadline, **fields.get("due_date", None)
            )
        )

        return instance

    def get_mixed_deadline(self, deadline_id):
        try:
            return MixedDeadline.objects.get(deadline_ptr=deadline_id)
        except MixedDeadline.DoesNotExist:
            raise Http404

    @transaction.atomic
    def get_or_create_deadline_flag(
        self, request, deadline: Deadline, default_deadline_flag: DefaultDeadlineFlag
    ) -> DeadlineFlag:
        instance = DeadlineFlag.objects.safe_get(
            parent=default_deadline_flag, deadline=deadline
        )
        if instance:
            return instance

        default_deadline_flag = (
            self.default_deadline_service.get_or_create_default_flag(
                instance=default_deadline_flag,
                **{
                    "name": default_deadline_flag.name,
                    "label": default_deadline_flag.label,
                    "index": default_deadline_flag.index,
                    "flag": default_deadline_flag.flag,
                },
            )
        )

        instance = DeadlineFlag()

        instance.parent = default_deadline_flag
        instance.deadline = deadline
        instance.flag = default_deadline_flag.flag

        instance.full_clean()
        instance.save()

        return instance

    @transaction.atomic
    def link_to_visum(self, request, visum: CampVisum):
        camp_year = visum.category_set.parent.camp_year_category_set.camp_year
        camp_type = visum.category_set.parent.camp_type

        default_deadline_set: DefaultDeadlineSet = DefaultDeadlineSet.objects.safe_get(
            camp_year=camp_year, camp_type=camp_type
        )
        if not default_deadline_set:
            raise Http404(
                "Unable to find default deadline set for camp year {} and camp type {}".format(
                    camp_year.year, camp_type.camp_type
                )
            )

        default_deadlines: List[
            DefaultDeadline
        ] = default_deadline_set.default_deadlines.all()
        logger.debug(
            "Found %d DefaultDeadline instances in set %s with camp year %s and camp type %s",
            len(default_deadlines),
            default_deadline_set.id,
            camp_year.year,
            camp_type.camp_type,
        )
        for default_deadline in default_deadlines:
            deadline_fields = DeadlineFactory.get_deadline_fields(
                default_deadline=default_deadline
            )
            if default_deadline.is_deadline():
                self._link_deadline_to_visum(
                    request, default_deadline, visum, deadline_fields
                )

            elif default_deadline.is_sub_category_deadline():
                self._link_sub_category_deadline_to_visum(
                    request, default_deadline, visum, deadline_fields
                )
            elif default_deadline.is_check_deadline():
                self._link_check_deadline_to_visum(
                    request, default_deadline, visum, deadline_fields
                )
            elif default_deadline.is_mixed_deadline():
                self._link_mixed_deadline_to_visum(
                    request, default_deadline, visum, deadline_fields
                )
            else:
                raise Http404(
                    "Unknown deadline type: {}".format(default_deadline.deadline_type)
                )

    def _link_deadline_to_visum(
        self,
        request,
        default_deadline: DefaultDeadline,
        visum: CampVisum,
        deadline_fields: dict,
    ):
        logger.debug(
            "Setting up Deadline %s (%s) with type %s for visum %s",
            default_deadline.name,
            default_deadline.id,
            default_deadline.deadline_type,
            visum.id,
        )
        deadline: Deadline = self.get_or_create_deadline(
            request=request,
            default_deadline=default_deadline,
            visum=visum,
            **deadline_fields,
        )
        default_flags: List[DefaultDeadlineFlag] = default_deadline.default_flags.all()
        logger.debug(
            "Found %d DefaultDeadlineFlag instances for DefaultDeadline %s",
            len(default_flags),
            default_deadline.name,
        )
        for default_flag in default_flags:
            flag = self.get_or_create_deadline_flag(
                request, deadline=deadline, default_deadline_flag=default_flag
            )
            deadline.flags.add(flag)

    def _link_sub_category_deadline_to_visum(
        self,
        request,
        default_deadline: DefaultDeadline,
        visum: CampVisum,
        deadline_fields: dict,
    ):
        logger.debug(
            "Setting up LinkedSubCategoryDeadline %s (%s) with type %s for visum %s",
            default_deadline.name,
            default_deadline.id,
            default_deadline.deadline_type,
            visum.id,
        )
        deadline: LinkedSubCategoryDeadline = (
            self.get_or_create_linked_sub_category_deadline(
                request=request,
                default_deadline=default_deadline,
                visum=visum,
                **deadline_fields,
            )
        )
        self._link_sub_categories_to_deadline(default_deadline, visum, deadline)

    def _link_check_deadline_to_visum(
        self,
        request,
        default_deadline: DefaultDeadline,
        visum: CampVisum,
        deadline_fields: dict,
    ):
        logger.debug(
            "Setting up LinkedCheckDeadline %s (%s) with type %s for visum %s",
            default_deadline.name,
            default_deadline.id,
            default_deadline.deadline_type,
            visum.id,
        )
        deadline: LinkedCheckDeadline = self.get_or_create_linked_check_deadline(
            request,
            default_deadline=default_deadline,
            visum=visum,
            **deadline_fields,
        )

        self._link_checks_to_deadline(default_deadline, visum, deadline)

    def _link_mixed_deadline_to_visum(
        self,
        request,
        default_deadline: DefaultDeadline,
        visum: CampVisum,
        deadline_fields: dict,
    ):
        logger.debug(
            "Setting up MixedDeadline %s (%s) with type %s for visum %s",
            default_deadline.name,
            default_deadline.id,
            default_deadline.deadline_type,
            visum.id,
        )
        deadline: MixedDeadline = self.get_or_create_mixed_deadline(
            request,
            default_deadline=default_deadline,
            visum=visum,
            **deadline_fields,
        )

        self._link_sub_categories_to_deadline(default_deadline, visum, deadline)
        self._link_checks_to_deadline(default_deadline, visum, deadline)

    def _link_sub_categories_to_deadline(
        self, default_deadline: DefaultDeadline, visum: CampVisum, deadline
    ):
        sub_categories: List[SubCategory] = default_deadline.sub_categories.all()
        logger.debug(
            "Found %d SubCategory instances linked to DefaultDeadline %s",
            len(sub_categories),
            default_deadline.name,
        )
        for sub_category in sub_categories:
            linked_sub_category: LinkedSubCategory = LinkedSubCategory.objects.safe_get(
                parent=sub_category, visum=visum
            )
            if not linked_sub_category:
                raise Http404(
                    "Unable to find LinkedSubCategory with parent SubCategory id {}".format(
                        sub_category.id
                    )
                )
            deadline.linked_sub_categories.add(linked_sub_category)

    def _link_checks_to_deadline(
        self, default_deadline: DefaultDeadline, visum: CampVisum, deadline
    ):
        checks: List[Check] = default_deadline.checks.all()
        logger.debug(
            "Found %d Check instances linked to DefaultDeadline %s",
            len(checks),
            default_deadline.name,
        )
        for check in checks:
            linked_check: LinkedCheck = LinkedCheck.objects.safe_get(
                parent=check, visum=visum
            )
            if not linked_check:
                raise Http404(
                    "Unable to find LinkedCheck with parent Check id {}".format(
                        check.id
                    )
                )
            deadline.linked_checks.add(linked_check)

    def list_for_visum(self, visum: CampVisum) -> List[Deadline]:
        deadlines: List[Deadline] = Deadline.objects.filter(visum=visum)
        results = list()

        for deadline in deadlines:
            if deadline.parent.is_deadline():
                results.append(Deadline.objects.get(id=deadline.id))
            elif deadline.parent.is_sub_category_deadline():
                results.append(
                    LinkedSubCategoryDeadline.objects.get(deadline_ptr=deadline.id)
                )
            elif deadline.parent.is_check_deadline():
                results.append(
                    LinkedCheckDeadline.objects.get(deadline_ptr=deadline.id)
                )
            elif deadline.parent.is_mixed_deadline():
                results.append(MixedDeadline.objects.get(deadline_ptr=deadline.id))

        return results
