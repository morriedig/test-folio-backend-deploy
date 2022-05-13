import datetime
import json
import os
from collections import OrderedDict

from django.test import Client, TestCase
from engine.models import *
from IAM.models import *

# Create your tests here.

# python manage.py test engine.tests.StockCase --settings=folio_backend.settings_test
# python manage.py test engine.tests.FollowCase --settings=folio_backend.settings_test
class StockCase(TestCase):
    # fixtures = ['fixture.json']
    def setUp(self) -> None:
        # 辦帳號
        print("setUp")
        self.c = Client()
        self.HOST = "http://localhost:8000/"
        url = os.path.join(self.HOST, "auth/login")
        MyUser.objects.create_user(account="test_user", password="password", email="kevin19981031@gmail.com")
        python_dict = {"account": "test_user", "password": "password"}
        self.resp = self.c.post(url, json.dumps(python_dict), content_type="application/json")
        self.token = self.resp.data["access"]
        # 塞假資料
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

    # def tearDown(self) -> None: #測試完後面如果要做什麼放這，沒有就算了
    #     print("後置tearDown2")

    def test_stock_get1(self):
        url = os.path.join(self.HOST, "/api/stock/?code=s01")
        answer = [
            OrderedDict(
                [("code", "s01"), ("name", "公司1"), ("last_price", 110.0), ("last_day_change", 0.09090909090909091)]
            )
        ]
        resp_200 = self.c.get(url, **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"})
        self.assertEqual(resp_200.status_code, 200)
        self.assertEqual(resp_200.data, answer)

        url = os.path.join(self.HOST, "/api/stock/")
        resp_400 = self.c.get(url, **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"})
        self.assertEqual(resp_400.status_code, 400)


class FollowCase(TestCase):
    def setUp(self) -> None:
        # 辦帳號
        print("setUp")
        self.c = Client()
        self.HOST = "http://localhost:8000/"
        url = os.path.join(self.HOST, "auth/login")
        MyUser.objects.create_user(account="test_provider", password="password", email="kevin19981031@gmail.com")
        MyUser.objects.create_user(account="test_follower", password="password", email="r10725021@ntu.edu.tw")

        python_dict = {"account": "test_provider", "password": "password"}
        self.resp_provider = self.c.post(url, json.dumps(python_dict), content_type="application/json")
        python_dict = {"account": "test_follower", "password": "password"}
        self.resp_follower = self.c.post(url, json.dumps(python_dict), content_type="application/json")
        self.token = self.resp_follower.data["access"]
        self.token_provider = self.resp_provider.data["access"]

        # 塞假資料
        s1 = Stock(code="s01", name="公司1")
        s1.save()
        sp1 = Stockprice(
            stock=Stock.objects.get(code="s01"),
            price=100,
            time=datetime.datetime(2022, 3, 1, 0, 0, 0),
        )
        sp1.save()
        u1 = MyUser.objects.filter(account="test_provider")[0]
        p1 = Portfolio(
            name="投資組合1",
            description="測試用",
            owner=u1,
            budget=5000,
            is_public=True,
            is_alive=True,
            follow_price=10,
        )
        p1.save()
        self.pid = Portfolio.objects.filter(name="投資組合1")[0].id

    def test_follow_post(self):
        url = os.path.join(self.HOST, "/api/follow/")
        provider_budget_old = MyUser.objects.filter(account="test_provider")[0].budget
        follower_budget_old = MyUser.objects.filter(account="test_follower")[0].budget
        portfolio_follow_price = Portfolio.objects.filter(name="投資組合1")[0].follow_price

        # 預算爆表的 follow 會不會過
        python_dict = {"pid": self.pid, "budget": 100000000}
        resp_402 = self.c.post(
            url,
            json.dumps(python_dict),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )
        self.assertEqual(resp_402.status_code, 402)

        # 合法請求
        budget = 100
        python_dict = {"pid": self.pid, "budget": budget}
        resp_200 = self.c.post(
            url,
            json.dumps(python_dict),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )
        self.assertEqual(resp_200.status_code, 200)

        # 重複 follow
        resp_409 = self.c.post(
            url,
            json.dumps(python_dict),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )
        self.assertEqual(resp_409.status_code, 409)

        # provider 是否成功拿到錢
        provider_budget_new = MyUser.objects.filter(account="test_provider")[0].budget
        self.assertEqual(provider_budget_old + portfolio_follow_price, provider_budget_new)

        # follow 是否成功付款
        follower_budget_new = MyUser.objects.filter(account="test_follower")[0].budget
        self.assertEqual(follower_budget_old - portfolio_follow_price - budget, follower_budget_new)

    def test_follow_get(self):

        # 生一個 follow
        url = os.path.join(self.HOST, "/api/follow/")
        python_dict = {"pid": self.pid, "budget": 100}
        resp_200 = self.c.post(
            url,
            json.dumps(python_dict),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"},
        )

        # 合法拿自己的follow
        resp_200 = self.c.get(url, **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"})
        self.assertEqual(resp_200.status_code, 200)
        self.assertEqual(resp_200.data[0]["is_alive"], True)

        # 非持有者拿 portfolio 的 follower
        url = os.path.join(self.HOST, "/api/follow/?pid=1")
        resp_401 = self.c.get(url, **{"HTTP_AUTHORIZATION": f"Bearer {self.token}"})
        self.assertEqual(resp_401.status_code, 401)

        # 合法拿 portfolio 的 follower
        resp_200 = self.c.get(url, **{"HTTP_AUTHORIZATION": f"Bearer {self.token_provider}"})
        self.assertEqual(resp_200.status_code, 200)
