from django.db import models

# https://stackoverflow.com/a/1490069
class SimpleChoiceField(models.IntegerField):
    val_to_choice: dict
    choice_to_val: dict

    def __init__(self, choices, **kwargs):
        if not hasattr(choices[0], "__iter__"):
            choices = zip(range(len(choices)), choices)

        self.val_to_choice = dict(choices)
        self.choice_to_val = dict((v, k) for k, v in choices)

    def to_python(self, value):
        return self.val_to_choice[value]

    def get_db_prep_value(self, choice):
        return self.choice_to_val[choice]
