from django.db import models


class Customer(models.Model):
    tenant_id = models.IntegerField()
    name = models.CharField(max_length=100)
