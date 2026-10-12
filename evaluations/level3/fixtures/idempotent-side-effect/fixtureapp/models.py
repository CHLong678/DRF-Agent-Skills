from django.db import models


class PaymentEffect(models.Model):
    idempotency_key = models.CharField(max_length=100)
    amount = models.IntegerField()
