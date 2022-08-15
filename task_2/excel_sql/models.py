from django.db import models


class UploadedFile(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    header = models.CharField(max_length=500)


class Class(models.Model):
    # contains only values from 1 to 9
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=200)


class Subclass(models.Model):
    # contains only values from 10 to 99
    id = models.SmallIntegerField(primary_key=True)
    cls = models.ForeignKey(Class, on_delete=models.CASCADE)


class BalanceAccount(models.Model):
    id = models.IntegerField(primary_key=True)
    # contains only values from 1000 to 9999
    # (not a primary key as we can have the same account numbers in different files)
    account_num = models.SmallIntegerField()
    subcls = models.ForeignKey(Subclass, on_delete=models.CASCADE)
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)


class OpeningBalance(models.Model):
    account = models.ForeignKey(BalanceAccount, primary_key=True, on_delete=models.CASCADE)
    assets = models.DecimalField(max_digits=19, decimal_places=2)
    liability = models.DecimalField(max_digits=19, decimal_places=2)


class Turnover(models.Model):
    account = models.ForeignKey(BalanceAccount, primary_key=True, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=19, decimal_places=2)
    credit = models.DecimalField(max_digits=19, decimal_places=2)
