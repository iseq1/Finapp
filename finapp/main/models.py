from django.db import models
from registration.models import CustomUser, UserProfile


class Category(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)


class Subcategory(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)


class Cash_box(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)


class Income(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    total = models.FloatField()
    date = models.DateField()
    comment = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cash_box = models.ForeignKey(Cash_box, on_delete=models.CASCADE)


class Expenses(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    total = models.FloatField()
    date = models.DateField()
    comment = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cash_box = models.ForeignKey(Cash_box, on_delete=models.CASCADE)



class Expenses_statistic(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.FloatField()
    percentage = models.FloatField()
    count_of_transactions = models.IntegerField()
    average_transaction = models.FloatField()
    last_transaction = models.CharField(max_length=255, null=True)
    max_transaction = models.CharField(max_length=255, null=True)
    min_transaction = models.CharField(max_length=255, null=True)
    monthly_difference = models.FloatField()


class Income_statistic(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.FloatField()
    percentage = models.FloatField()
    count_of_transactions = models.IntegerField()
    average_transaction = models.FloatField()
    monthly_difference = models.FloatField()
    revenue_growth_rate = models.FloatField()


