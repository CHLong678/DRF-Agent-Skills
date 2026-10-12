from django.db import models


class Order(models.Model):
    tenant_id = models.IntegerField()
    code = models.CharField(max_length=50)
