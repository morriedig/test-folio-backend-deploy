import datetime

import pandas as pd

# from datetime import timedelta
import pytz
import twstock
from django.shortcuts import render

from .models import *


def insert_test_data(request):
    u1 = User(
        name="provider1",
        bankaccount="123456789123",
        email="r10725020@ntu.edu.tw",
        password="password",
        id_number="A123456789",
    )
    u2 = User(
        name="follower1",
        bankaccount="234567891234",
        email="b06705004@ntu.edu.tw",
        password="password",
        id_number="A123456780",
    )
    p1 = Portfolio(
        name="投資組合1",
        description="測試用",
        owner=u1,
        budget=5000,
        cash=5000,
        is_public=True,
        is_alive=True,
    )
    s1 = Stock(code="s01", name="公司1")
    u1.save()
    u2.save()
    p1.save()
    s1.save()
    # test_message = Stock.objects.filter(id=1)
    # return render(request, "insert_test.html", locals())
    sp1 = Stockprice(
        stock=Stock.objects.filter(id=1)[0],
        price=100,
        time=datetime.datetime(2022, 3, 1, 0, 0, 0),
    )
    t1 = Transaction(
        portfolio=Portfolio.objects.filter(id=1)[0],
        stock=Stock.objects.filter(id=1)[0],
        amount=10,
        price=100,
        time=datetime.datetime(2022, 3, 1, 23, 55, 59),
    )
    f1 = Follow(
        portfolio=Portfolio.objects.filter(id=1)[0],
        user=User.objects.filter(id=1)[0],
        starttime=datetime.datetime(2022, 2, 1, 23, 55, 59),
        endtime=datetime.datetime(2022, 4, 1, 23, 55, 59),
        budget=1000,
        cash=1000,
        is_alive=True,
        stop_limit=0.1,
    )
    sp1.save()
    t1.save()
    f1.save()

    test_message = "insert fake data done"
    return render(request, "insert_test.html", locals())


def insert_stock(request):
    twstocks = pd.read_csv("engine/twse_equities.csv")
    stocks = twstocks[(twstocks["market"] == "上市") & (twstocks["type"] == "股票")]
    for i, stock in stocks.iterrows():
        s = Stock(code=stock["code"], name=stock["name"], group=stock["group"])
        s.save()
    # cash
    s = Stock(code="0000", name="cash", group="現金")
    s.save()

    test_message = "insert stock done"
    return render(request, "insert_test.html", locals())


def insert_stock_price(request):
    stocks = Stock.objects.all()
    m = ""
    # stocks
    for i, target_stock in enumerate(stocks):
        if target_stock.code == "s01":
            continue
        sid = target_stock.id
        stock = twstock.Stock(target_stock.code)
        target_price = stock.fetch_from(2022, 3)  # 取用2022/03至今每天的交易資料
        stock_data = [[tp.date, tp.close] for tp in target_price]
        for sd in stock_data:
            if sd[1] != None:
                sp = Stockprice(
                    stock=Stock.objects.filter(id=sid)[0],
                    price=sd[1],
                    time=sd[0].replace(tzinfo=pytz.UTC),
                )
                sp.save()
        m += str(target_stock.code) + "\n"
        if i == 100:
            break
    # cash
    base = datetime.datetime.today()
    gap = base - datetime.datetime(2022, 3, 1)
    date_list = [base - datetime.timedelta(days=x) for x in range(gap.days + 1)]
    date_list = [x.replace(hour=0, minute=0, second=0, microsecond=0) for x in date_list][::-1]
    for dt in date_list:
        cash = Stockprice(
            stock=Stock.objects.filter(code="0000")[0],
            price=1,
            time=dt.replace(tzinfo=pytz.UTC),
        )
        cash.save()
    m += "cash"
    test_message = "insert stock:\n" + str(m) + "price done"
    return render(request, "insert_test.html", locals())
