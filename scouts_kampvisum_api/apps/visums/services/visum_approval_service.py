
from typing import List

from django.db.models import Q

from apps.visums.models import LinkedSubCategory, CampVisum
from apps.visums.models.enums import CampVisumApprovalState, CampVisumState


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)

class CampVisumApprovalService:
    
    def update_feedback(self, request, instance: LinkedSubCategory, feedback: str):
        logger.debug(
            "Setting feedback on LinkedSubCategory %s (%s)",
            instance.parent.name,
            instance.id,
        )
        
        instance.feedback = feedback
        instance.updated_by = request.user

        instance.full_clean()
        instance.save()
        
        return instance

    def update_approval(self, request, instance: LinkedSubCategory, approval: str):
        approval: CampVisumApprovalState = CampVisumApprovalState.get_state(approval)

        logger.debug(
            "Setting approval state %s (%s) on LinkedSubCategory %s (%s)",
            approval[1],
            approval[0],
            instance.parent.name,
            instance.id,
        )

        instance.approval = approval[0]
        instance.updated_by = request.user

        instance.full_clean()
        instance.save()
        
        # Set proper state on camp visum
        visum: CampVisum = instance.category.category_set.visum
        state: CampVisumState = CampVisumState.SIGNABLE
        
        if approval[1] == CampVisumApprovalState.DISAPPROVED.label:    
            logger.debug("LinkedSubCategory %s (%s) is DISAPPROVED, setting CampVisum %s (%s) to state NOT_SIGNABLE", instance.parent.name, instance.id, visum.camp.name, visum.id)
            
            state = CampVisumState.NOT_SIGNABLE
        else:
            disapproved_sub_categories: List[LinkedSubCategory] = LinkedSubCategory.objects.all().filter(Q(category__category_set__visum=visum)&Q(approval=CampVisumApprovalState.DISAPPROVED))
            if disapproved_sub_categories.count() > 0:
                state = CampVisumState.NOT_SIGNABLE
            else:
                state = CampVisumState.SIGNABLE
        
        visum.state = state
            
        visum.full_clean()
        visum.save()
        
        return instance
    
    def update_dc_notes(self, request, instance: CampVisum, notes: str):
        logger.debug(
            "Adding DC notes on CampVisum %s (%s)",
            instance.camp.name,
            instance.id,
        )

        instance.notes = notes
        instance.updated_by = request.user

        instance.full_clean()
        instance.save()
        
        return instance