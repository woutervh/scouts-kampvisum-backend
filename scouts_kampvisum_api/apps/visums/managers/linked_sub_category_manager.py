from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

from apps.visums.models.enums import CampVisumApprovalState


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedSubCategoryQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def all(self, *args, **kwargs):
        return super().all(args, is_archived=False, **kwargs)

    def disapproved(self, visum):
        return self.filter(Q(category__category_set__visum=visum)&Q(approval=CampVisumApprovalState.DISAPPROVED))

    def approvable(self, visum):
        return self.filter(category__category_set__visum=visum).exclude(approval=CampVisumApprovalState.DISAPPROVED)

    def globally_approvable(self, visum):
        return self.filter(category__category_set__visum=visum).exclude(approval=CampVisumApprovalState.DISAPPROVED).exclude(approval=CampVisumApprovalState.APPROVED_FEEDBACK)
    
    def resolution_not_required(self, visum):
        return self.filter(category__category_set__visum=visum).exclude(approval=CampVisumApprovalState.DISAPPROVED).exclude(approval=CampVisumApprovalState.APPROVED_FEEDBACK).exclude(approval=CampVisumApprovalState.FEEDBACK_RESOLVED)
    
    def requires_resolution(self, visum):
        return self.filter(Q(category__category_set__visum=visum)&Q(approval=CampVisumApprovalState.DISAPPROVED))
    
    def can_be_resolved(self, visum):
        return self.filter(Q(category__category_set__visum=visum)&(Q(approval=CampVisumApprovalState.DISAPPROVED)|Q(approval=CampVisumApprovalState.APPROVED_FEEDBACK)))


class LinkedSubCategoryManager(models.Manager):
    """
    Loads LinkedSubCategory instances by their name, not their id.
    """

    def get_queryset(self):
        return LinkedSubCategoryQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        category = kwargs.get("category", None)
        parent = kwargs.get("parent", None)
        visum = kwargs.get("visum", None)
        is_archived = kwargs.get("is_archived", False)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if category and parent:
            try:
                return self.get_queryset().get(parent=parent, category=category)
            except:
                pass

        if parent and visum:
            try:
                return self.get_queryset().get(
                    parent__id=parent.id,
                    category__category_set__visum__id=visum.id,
                    is_archived=is_archived,
                )
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate LinkedSubCategory instance(s) with provided params (id: {}, (category: {}, parent: {}), (parent: {}, visum: {})".format(
                    pk,
                    category.to_simple_str() if category else None,
                    parent.to_simple_str() if parent else None,
                    parent.to_simple_str() if parent else None,
                    visum,
                )
            )
        return None
