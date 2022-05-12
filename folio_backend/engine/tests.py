import datetime
import json
from collections import OrderedDict

from django.test import Client, TestCase
from engine.models import *
from IAM.models import *

# Create your tests here.

# python manage.py test --settings=folio_backend.settings_test
class StockCase(TestCase):
    # fixtures = ['fixture.json']
    def setUp(self) -> None:
        # 辦帳號
        print("setUp")
        self.c = Client()
        MyUser.objects.create_user(account="test_provider", password="password", email="kevin19981031@gmail.com")
        python_dict = {"account": "test_provider", "password": "password"}
        s1 = Stock(code="s01", name="公司1")
        s1.save()
        sp1 = Stockprice(
            stock=Stock.objects.get(code="s01"),
            price=100,
            time=datetime.datetime(2022, 3, 1, 0, 0, 0),
        )
        sp2 = Stockprice(
            stock=Stock.objects.get(code="s01"),
            price=110,
            time=datetime.datetime(2022, 3, 2, 0, 0, 0),
        )
        sp1.save()
        sp2.save()

        url = "http://127.0.0.1:8000/auth/login"
        self.resp = self.c.post(url, json.dumps(python_dict), content_type="application/json")
        # print(self.resp.data)

    def tearDown(self) -> None:
        print("後置tearDown2")

    def test_stock_get(self):
        token = self.resp.data["access"]
        url = "http://127.0.0.1:8000/api/stock/?code=s01"
        answer = [
            OrderedDict(
                [("code", "s01"), ("name", "公司1"), ("last_price", 110.0), ("last_day_change", 0.09090909090909091)]
            )
        ]
        resp_stock = self.c.get(url, **{"HTTP_AUTHORIZATION": f"Bearer {token}"})
        self.assertEqual(resp_stock.data, answer)
