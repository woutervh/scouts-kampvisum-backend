from django.db import models


class PaymentStatus(models.TextChoices):
    """
    An enum that indicates wether a participant has payed
    """

    PAYED = "Y", "YES"
    NOT_PAYED = "N", "NO"
    NOT_APPLICABLE = "X", "NOT_APPLICABLE"

    @staticmethod
    def endpoint_from_type(payment_status):
        if isinstance(payment_status, bool):
            if payment_status:
                return PaymentStatus.PAYED
            return PaymentStatus.NOT_PAYED

        for option in PaymentStatus.choices:
            if option[0] == payment_status:
                return option[1]
        return None
