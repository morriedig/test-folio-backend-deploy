# from django.db import models

# Create your models here.
from django.db import models


class Follow(models.Model):
    fid = models.TextField(primary_key=True)
    portfolio = models.ForeignKey("Portfolio", models.CASCADE, db_column="portfolio")
    user = models.ForeignKey("User", models.CASCADE, db_column="user")
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    f_budget = models.FloatField()
    stop_limit = models.FloatField()
    is_alive = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = "follow"
        # unique_together = (("portfolio", "user"),)


class Portfolio(models.Model):
    pid = models.TextField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    owner = models.ForeignKey("User", models.CASCADE, db_column="owner")
    p_budget = models.FloatField()
    is_public = models.BooleanField(default=False)
    is_alive = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = "portfolio"


class Stock(models.Model):
    sid = models.TextField(primary_key=True)
    name = models.TextField()
    group = models.TextField()

    class Meta:
        managed = True
        db_table = "stock"


class Stockprice(models.Model):
    spid = models.TextField(primary_key=True)
    stock = models.ForeignKey(Stock, models.CASCADE, db_column="stock")
    time = models.DateTimeField()
    price = models.FloatField()

    class Meta:
        managed = True
        db_table = "stockprice"
        # unique_together = (("stock", "time"),)


class Transaction(models.Model):
    tid = models.TextField(primary_key=True)
    portfolio = models.ForeignKey(Portfolio, models.CASCADE, db_column="portfolio")
    stock = models.ForeignKey(Stock, models.CASCADE, db_column="stock")
    amount = models.FloatField()
    time = models.DateTimeField()
    price = models.FloatField()

    class Meta:
        managed = True
        db_table = "transaction"
        # unique_together = (("portfolio", "stock"),)


class User(models.Model):
    uid = models.TextField(primary_key=True)
    name = models.TextField()
    bankaccount = models.TextField()
    email = models.TextField()
    password = models.TextField()
    u_budget = models.FloatField(blank=True, null=True)
    id_number = models.TextField()

    class Meta:
        managed = True
        db_table = "user"
