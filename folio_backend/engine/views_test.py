import datetime
import pandas as pd
# from datetime import timedelta
import pytz
import twstock
from django.shortcuts import render

from .models import *


def insert_test_data(request):
    u1 = User(
        uid="u0001",
        name="provider1",
        bankaccount="123456789123",
        email="r10725021@ntu.edu.tw",
        password="password",
        u_budget=10000,
        id_number="A123456789",
    )
    u2 = User(
        uid="u0002",
        name="follower1",
        bankaccount="234567891234",
        email="b06705004@ntu.edu.tw",
        password="password",
        u_budget=5000,
        id_number="A123456780",
    )
    p1 = Portfolio(
        pid="p0001",
        name="投資組合1",
        description="測試用",
        owner=u1,
        p_budget=5000,
        is_public=True,
        is_alive=True,
    )
    s1 = Stock(sid="s0001", name="公司1")
    u1.save()
    u2.save()
    p1.save()
    s1.save()
    sp1 = Stockprice(
        spid="sp0001",
        stock=Stock.objects.filter(sid="s0001")[0],
        price=100,
        time=datetime.datetime(2015, 10, 9, 23, 55, 59),
    )
    t1 = Transaction(
        tid="t0001",
        portfolio=Portfolio.objects.filter(pid="p0001")[0],
        stock=Stock.objects.filter(sid="s0001")[0],
        amount=10,
        price=100,
        time=datetime.datetime(2015, 10, 9, 23, 55, 59),
    )
    f1 = Follow(
        fid="f0001",
        portfolio=Portfolio.objects.filter(pid="p0001")[0],
        user=User.objects.filter(uid="u0002")[0],
        starttime=datetime.datetime(2015, 10, 8, 23, 55, 59),
        endtime=datetime.datetime(2015, 11, 7, 23, 55, 59),
        f_budget=1000,
        is_alive=True,
        stop_limit=0.1,
    )
    sp1.save()
    t1.save()
    f1.save()

    test_message = "insert fake data done"
    return render(request, "insert_test.html", locals())


def insert_stock(request):
    twstocks = pd.read_csv('engine/twse_equities.csv')
    stocks = twstocks[(twstocks['market'] == "上市") & (twstocks['type'] == "股票")]
    for i,stock in stocks.iterrows():
        s = Stock(sid=stock['code'], name=stock['name'], group=stock['group'])
        s.save()
    test_message = "insert stock done"
    return render(request, "insert_test.html", locals())


def insert_stock_price(request):
    stocks = Stock.objects.all()
    m = ""
    for i, target_stock in enumerate(stocks):
        if target_stock.sid == "s0001":
            continue
        sid = target_stock.sid
        stock = twstock.Stock(sid)
        target_price = stock.fetch_from(2022, 3)  # 取用2022/03至今每天的交易資料
        stock_data = [[tp.date, tp.close] for tp in target_price]
        for sd in stock_data:
            if sd[1] != None:
                sp = Stockprice(
                    spid=str(target_stock.sid) + str(sd[0].replace(tzinfo=pytz.UTC)),
                    stock=Stock.objects.filter(sid=sid)[0],
                    price=sd[1],
                    time=sd[0].replace(tzinfo=pytz.UTC),
                )
                sp.save()
        m += str(target_stock.sid) + '\n'
        if i == 100:
            break
    test_message = "insert stock:\n" + str(m) + "price done"
    return render(request, "insert_test.html", locals())
