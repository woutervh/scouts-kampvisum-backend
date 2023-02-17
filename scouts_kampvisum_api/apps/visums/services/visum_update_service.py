from django.utils import timezone

from apps.visums.models import (
    LinkedSubCategory,
    LinkedCategory,
    LinkedCategorySet,
    CampVisum,
)
from apps.visums.models.enums import CheckState


class CampVisumUpdateService:

    def update_sub_category(self, request, instance: LinkedSubCategory, now=None):

        instance.check_state = CheckState.CHECKED if LinkedSubCategory.objects.has_unchecked_checks(
            pk=instance.id) else CheckState.UNCHECKED
        instance.updated_by = request.user
        instance.updated_on = now if now else timezone.now()

        instance.full_clean()
        instance.save()

        self.update_category(
            request=request, instance=instance.category, now=now)

        return instance

    def update_category(self, request, instance: LinkedCategory, now=None):
        instance.check_state = CheckState.CHECKED if LinkedCategory.objects.has_unchecked_checks(
            pk=instance.id) else CheckState.UNCHECKED
        instance.updated_by = request.user
        instance.updated_on = now if now else timezone.now()

        instance.full_clean()
        instance.save()

        self.update_category_set(
            request=request, instance=instance.category_set, now=now)

        return instance

    def update_category_set(self, request, instance: LinkedCategorySet, now=None):
        instance.check_state = CheckState.CHECKED if LinkedCategorySet.objects.has_unchecked_checks(
            pk=instance.id) else CheckState.UNCHECKED
        instance.updated_by = request.user
        instance.updated_on = now if now else timezone.now()

        instance.full_clean()
        instance.save()

        self.update_visum(request=request, instance=instance.visum, now=now)

        return instance

    def update_visum(self, request, instance: CampVisum, now=None):
        instance.check_state = CheckState.CHECKED if CampVisum.objects.has_unchecked_checks(
            pk=instance.id) else CheckState.UNCHECKED
        instance.updated_by = request.user
        instance.updated_on = now if now else timezone.now()

        instance.full_clean()
        instance.save()

        return instance
