from django.db import models

from apps.deadlines.models import DeadlineDate

from apps.visums.models import CampVisum, LinkedSubCategory, LinkedCheck

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField
from scouts_auth.inuits.models.interfaces import Describable, Explainable, Translatable


class Deadline(Describable, Explainable, Translatable, AuditedBaseModel):
    
    visum = models.ForeignKey(CampVisum, on_delete=models.CASCADE, related_name="deadlines")
    name = RequiredCharField()
    is_important = models.BooleanField(default=False)
    due_date = DeadlineDate()
    
    def __str__(self) -> str:
        return "visum ({}), name ({}), important ({}), label ({}), description ({}), explanation ({})".format(self.visum.id, self.name, self.important, self.label, self.description, self.explanation)


class SubCategoryDeadline(Deadline):
    
    deadline_sub_category = models.ForeignKey(LinkedSubCategory, on_delete=models.CASCADE, related_name="deadline")
    
    def __str__(self) -> str:
        return "{}, sub_category ({})".format(super().__str__(), self.sub_category)

class CheckDeadline(Deadline):
    
    deadline_check = models.ForeignKey(LinkedCheck, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return "{}, check ({})".format(super().__str__(), self.check)

class DeadlineDependentDeadline(Deadline):
    
    deadline_due_after_deadline = models.ForeignKey(Deadline, on_delete=models.CASCADE, related_name="deadline")
    
    def __str__(self) -> str:
        return "{}, due_after_deadline ({})".format(super().__str__(), self.due_after_deadline)
