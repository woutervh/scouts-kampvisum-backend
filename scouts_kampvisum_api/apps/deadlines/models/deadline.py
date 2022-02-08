from django.db import models

from apps.deadlines.models import DefaultDeadline
from apps.deadlines.models.enums import DeadlineType
from apps.deadlines.managers import DeadlineManager

from apps.visums.models import CampVisum, LinkedSubCategory, LinkedCheck


class Deadline(DefaultDeadline):
    
    objects = DeadlineManager()
    
    visum = models.ForeignKey(CampVisum, on_delete=models.CASCADE, related_name="deadlines")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.deadline_type = DeadlineType.DEADLINE
    
    def __str__(self):
        return "visum ({}), {}".format(self.visum.id, super().__str__())


class SubCategoryDeadline(Deadline):
    
    deadline_sub_category = models.ForeignKey(LinkedSubCategory, on_delete=models.CASCADE, related_name="deadline")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.deadline_type = DeadlineType.SUB_CATEGORY
    
    def __str__(self) -> str:
        return "{}, sub_category ({})".format(super().__str__(), self.sub_category)

class CheckDeadline(Deadline):
    
    deadline_check = models.ForeignKey(LinkedCheck, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return "{}, check ({})".format(super().__str__(), self.check)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.deadline_type = DeadlineType.CHECK

class DeadlineDependentDeadline(Deadline):
    
    deadline_due_after_deadline = models.ForeignKey(Deadline, on_delete=models.CASCADE, related_name="deadline")
    
    def __str__(self) -> str:
        return "{}, due_after_deadline ({})".format(super().__str__(), self.due_after_deadline)
