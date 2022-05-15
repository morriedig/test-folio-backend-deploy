from django.db.models import Sum
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
