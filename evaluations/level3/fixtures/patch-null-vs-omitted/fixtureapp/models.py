from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    note = models.CharField(max_length=200, null=True, blank=True)
