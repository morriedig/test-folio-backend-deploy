from django.db.models import Sum
from django.utils import timezone as datetime
from engine.models import *


def getStockValue(pid):
    value = 0
    portfolio = Portfolio.objects.get(id=pid)
    transaction = Transaction.objects.filter(portfolio=portfolio).values("stock").annotate(total_amount=Sum("amount"))
    for stock in transaction:
        stockprice = Stockprice.objects.filter(stock=stock["stock"]).order_by("-time")[0]
        value += stock["total_amount"] * stockprice.price
    return value


def getCash(pid):
    value = 0
    portfolio = Portfolio.objects.get(id=pid)
    cash = Stock.objects.get(code="0000")
    transaction = Transaction.objects.filter(portfolio=portfolio, stock=cash)
    for tran in transaction:
        value += tran.amount
    return value


def checkBudget(uid, cash):
    user_budget = User.objects.get(id=uid).budget
    return cash <= user_budget


def getStock(pid):
    stock_list = list()
    stock_amount_list = list()
    portfolio = Portfolio.objects.get(id=pid)
    transaction = Transaction.objects.filter(portfolio=portfolio).values("stock").annotate(total_amount=Sum("amount"))
    for stock in transaction:
        stock_list.append(stock["stock"])
        stock_amount_list.append(stock["total_amount"])
    return stock_list, stock_amount_list


def getROI(pid, days):

    today = datetime.now()
    start_date = today - datetime.timedelta(days=days)
    portfolio = Portfolio.objects.get(id=pid)
    value_now = 0
    value_before = 0
    transaction_now = (
        Transaction.objects.filter(portfolio=portfolio).values("stock").annotate(total_amount=Sum("amount"))
    )
    transaction_before_start_time = (
        Transaction.objects.filter(portfolio=portfolio, time__lt=start_date)
        .values("stock")
        .annotate(total_amount=Sum("amount"))
    )

    for stock in transaction_now:
        stockprice = Stockprice.objects.filter(stock=stock["stock"]).order_by("-time")[0]
        value_now += stock["total_amount"] * stockprice.price
    for stock in transaction_before_start_time:
        stockprice = Stockprice.objects.filter(stock=stock["stock"]).order_by("-time")[0]
        value_before += stock["total_amount"] * stockprice.price

    roi = (value_now - value_before) / portfolio.budget
    return round(roi, 4) * 100
