from django.db import models


class Order(models.Model):
    code = models.CharField(max_length=50, unique=True)
