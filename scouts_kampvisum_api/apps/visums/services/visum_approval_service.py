from typing import List

from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.visums.models import LinkedSubCategory, CampVisum
from apps.visums.models.enums import CampVisumApprovalState, CampVisumState


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumApprovalService:
    def update_feedback(
        self, request, instance: LinkedSubCategory, feedback: str
    ) -> LinkedSubCategory:
        logger.debug(
            "Setting feedback on LinkedSubCategory %s (%s)",
            instance.parent.name,
            instance.id,
        )

        instance.feedback = feedback
        instance.updated_by = request.user
        instance.updated_on = timezone.now()

        instance.full_clean()
        instance.save()

        return instance

    def update_approval(
        self, request, instance: LinkedSubCategory, approval: str
    ) -> LinkedSubCategory:
        visum: CampVisum = instance.category.category_set.visum
        approval: CampVisumApprovalState = CampVisumApprovalState.get_state_enum(
            approval
        )

        logger.debug(
            "Setting approval state %s (%s) on LinkedSubCategory %s (%s) for CampVisum %s with state %s",
            approval,
            approval.label,
            instance.parent.name,
            instance.id,
            visum.camp.name,
            visum.state,
        )

        instance.approval = approval
        instance.updated_by = request.user
        instance.updated_on = timezone.now()

        instance.full_clean()
        instance.save()

        self._set_visum_state(
            request=request, instance=instance, approval=approval, visum=visum
        )

        return instance

    def handle_feedback(
        self, request, instance: LinkedSubCategory
    ) -> LinkedSubCategory:
        visum: CampVisum = instance.category.category_set.visum
        logger.debug(
            "Setting feedback as resolved on LinkedSubCategory %s (%s) for visum %s with state %s",
            instance.parent.name,
            instance.id,
            visum.camp.name,
            visum.state,
        )
        instance.approval = (
            CampVisumApprovalState.FEEDBACK_READ
            if instance.approval == CampVisumApprovalState.APPROVED_FEEDBACK
            else CampVisumApprovalState.FEEDBACK_RESOLVED
        )
        instance.updated_by = request.user
        instance.updated_on = timezone.now()

        instance.full_clean()
        instance.save()

        self._set_visum_state(
            request=request, instance=instance, approval=instance.approval, visum=visum
        )

        return instance

    def update_dc_notes(self, request, instance: CampVisum, notes: str) -> CampVisum:
        logger.debug(
            "Adding DC notes on CampVisum %s (%s) with state %s",
            instance.camp.name,
            instance.id,
            instance.state,
        )

        instance.notes = notes
        instance.updated_by = request.user
        instance.updated_on = timezone.now()

        instance.full_clean()
        instance.save()

        return instance

    def global_update_approval(
        self, request, instance: CampVisum, approval: CampVisumApprovalState = None
    ) -> CampVisum:
        approval = approval if approval else CampVisumApprovalState.APPROVED

        logger.debug(
            "Globally setting approval state %s for visum %s (%s)",
            approval,
            instance.camp.name,
            instance.id,
        )

        # if approval == CampVisumApprovalState.APPROVED:
        # approvable_sub_categories: List[
        #     LinkedSubCategory
        # ] = LinkedSubCategory.objects.all().globally_approvable(visum=instance)
        # for approvable_sub_category in approvable_sub_categories:
        #     approvable_sub_category.approval = approval
        #     instance.updated_by = request.user

        #     approvable_sub_category.full_clean()
        #     approvable_sub_category.save()

        instance = self._set_visum_state(
            request=request,
            instance=None,
            approval=approval,
            visum=instance,
            global_approval=True,
        )

        return instance

    def global_handle_feedback(self, request, instance: CampVisum) -> CampVisum:
        logger.debug(
            "Setting feedback as resolved on all sub-categories of CampVisum %s (%s)",
            instance.camp.name,
            instance.id,
        )
        now = timezone.now()

        resolvable_sub_categories: List[
            LinkedSubCategory
        ] = LinkedSubCategory.objects.all().can_be_resolved(visum=instance)
        for resolvable_sub_category in resolvable_sub_categories:
            resolvable_sub_category.approval = CampVisumApprovalState.FEEDBACK_RESOLVED
            resolvable_sub_category.updated_by = request.user
            resolvable_sub_category.updated_on = now

            resolvable_sub_category.full_clean()
            resolvable_sub_category.save()

        acknowledgeable_sub_categories: List[LinkedSubCategory] = LinkedSubCategory.objects.all(
        ).can_be_acknowledged(visum=instance)
        for acknowledgeable_sub_category in acknowledgeable_sub_categories:
            acknowledgeable_sub_category.approval = CampVisumApprovalState.FEEDBACK_READ
            acknowledgeable_sub_category.updated_by = request.user
            acknowledgeable_sub_category.updated_on = now

            acknowledgeable_sub_category.full_clean()
            acknowledgeable_sub_category.save()

        instance = self._set_visum_state(
            request=request,
            instance=None,
            approval=CampVisumApprovalState.FEEDBACK_RESOLVED,
            visum=instance,
        )

        return instance

    def _set_visum_state(
        self,
        request,
        instance: LinkedSubCategory,
        approval: CampVisumApprovalState,
        visum: CampVisum = None,
        global_approval: bool = False,
    ) -> CampVisum:
        # Set proper state on camp visum
        visum: CampVisum = visum if visum else instance.category.category_set.visum
        state: CampVisumApprovalState = None
        logger.debug(
            f"APPROVAL: {approval} (%s)",
            type(approval).__name__,
        )

        # feedback was resolved, check other sub-categories and set proper state on visum
        if approval == CampVisumApprovalState.FEEDBACK_RESOLVED:
            # leaders have acknowledged DC remarks (approval was APPROVED_FEEDBACK
            resolvable_sub_categories: List[
                LinkedSubCategory
            ] = LinkedSubCategory.objects.all().requires_resolution(visum=visum)
            # no more sub-categories that need resolution, set FEEDBACK_HANDLED on visum
            if resolvable_sub_categories.count() == 0:
                logger.debug(
                    "All resolvable sub-categories were handled, setting state FEEDBACK_HANDLED on CampVisum %s (%s)",
                    visum.camp.name,
                    visum.id,
                )
                state = CampVisumState.FEEDBACK_HANDLED
            else:
                state = CampVisumState.NOT_SIGNABLE
        else:
            # dc disapproved a sub-category, set proper state on visum
            if approval == CampVisumApprovalState.DISAPPROVED:
                logger.debug(
                    "Setting CampVisum %s (%s) to state NOT_SIGNABLE",
                    visum.camp.name,
                    visum.id,
                )

                state = CampVisumState.NOT_SIGNABLE
            else:
                if global_approval:
                    disapproved_sub_categories: List[
                        LinkedSubCategory
                    ] = LinkedSubCategory.objects.all().disapproved(visum=visum)
                    if disapproved_sub_categories.count() > 0:
                        state = CampVisumState.NOT_SIGNABLE
                    else:
                        # Party !
                        state = CampVisumState.APPROVED
                else:
                    state = visum.state

        if not state:
            raise ValidationError(
                "CampVisum needs to have a state, none given")

        visum.state = state
        visum.updated_by = request.user
        visum.updated_on = timezone.now()

        visum.full_clean()
        visum.save()
