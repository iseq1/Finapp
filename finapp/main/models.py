from django.db import models
from registration.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)


class Subcategory(models.Model):
    name = models.CharField(max_length=30)


class Income(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    total = models.FloatField()
    date = models.DateField()
    comment = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Expenses(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    total = models.FloatField()
    date = models.DateField()
    comment = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)