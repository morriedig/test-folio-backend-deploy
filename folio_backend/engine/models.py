# from django.db import models

# Create your models here.
from django.db import models


class Follow(models.Model):
    # id = models.BigIntegerField(primary_key = True)
    portfolio = models.ForeignKey("Portfolio", models.CASCADE, db_column="portfolio")
    user = models.ForeignKey("User", models.CASCADE, db_column="user")
    starttime = models.DateTimeField()
    # endtime = models.DateTimeField()
    budget = models.FloatField()
    # cash = models.FloatField()
    # stop_limit = models.FloatField()
    is_alive = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = "follow"
        # unique_together = (("portfolio", "user"),)


class Portfolio(models.Model):
    # id = models.BigIntegerField(primary_key = True)
    name = models.TextField(default="我是一個投資組合")
    description = models.TextField(default="世界你好")
    owner = models.ForeignKey("User", models.CASCADE, db_column="owner")
    follow_price = models.FloatField(default=1000, blank=True)
    budget = models.FloatField(default=10000, blank=True)
    is_public = models.BooleanField(default=False)
    is_alive = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = "portfolio"


class Stock(models.Model):
    # id = models.AutoField(primary_key = True)
    code = models.TextField()
    name = models.TextField()
    group = models.TextField()

    class Meta:
        managed = True
        db_table = "stock"


class Stockprice(models.Model):
    # id = models.BigIntegerField(primary_key = True)
    stock = models.ForeignKey(Stock, models.CASCADE, db_column="stock")
    time = models.DateTimeField()
    price = models.FloatField()

    class Meta:
        managed = True
        db_table = "stockprice"
        # unique_together = (("stock", "time"),)


class Transaction(models.Model):
    # id = models.BigIntegerField(primary_key = True)
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
    # id = models.BigIntegerField(primary_key = True)
    name = models.TextField(default="我是已閱讀並同意以上條款的帳號")
    bankaccount = models.TextField(default="123456789")
    email = models.TextField(default="iHaveNoEmail")
    password = models.TextField(default="")
    budget = models.FloatField(default=10000, null=True)
    id_number = models.TextField(default="A123456789", blank=True)

    class Meta:
        managed = True
        db_table = "user"
