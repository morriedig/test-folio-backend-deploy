from django.db.models import Q
from django.utils import timezone as datetime
from engine.models import *
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .transaction_serializers import Transactionserializer


# Create your views here.
class TransactionAPIView(GenericAPIView):
    serializer_class = Transactionserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **krgs):
        try:

            pid = request.query_params.get("pid", "")

            portfolio = Portfolio.objects.get(id=pid)
            owner = portfolio.owner
            user = request.user

            if owner != user:
                return Response("YOU CAN'T MAKE TRANSACTION FOR OTHER", status=status.HTTP_402_PAYMENT_REQUIRED)

            transaction = Transaction.objects.filter(portfolio=portfolio).all()
            ans = Transactionserializer(transaction, many=True)

            return Response(ans.data, status=status.HTTP_200_OK)
        except:
            return Response("SOMETHING WRONG IN REQUEST DATA", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **krgs):
        try:
            data = request.data
            stock_code = data["stock"]
            amount = data["cash"]
            pid = data["pid"]

            time = datetime.now()
            stock = Stock.objects.get(code=stock_code)
            price = Stockprice.objects.filter(stock=stock).last().price
            portfolio = Portfolio.objects.get(id=pid)
            owner = portfolio.owner
            user = request.user

            if owner != user:
                return Response("YOU CAN'T MAKE TRANSACTION FOR OTHER", status=status.HTTP_402_PAYMENT_REQUIRED)
            if portfolio.budget <= amount:
                return Response("NOT ENOUGH CASH", status=status.HTTP_402_PAYMENT_REQUIRED)
            portfolio.budget = portfolio.budget - amount
            portfolio.save()
            new_transaction = Transaction(portfolio=portfolio, stock=stock, amount=amount, time=time, price=price)

            new_transaction.save()

            return Response("SUCCESS", status=status.HTTP_200_OK)
        except:
            return Response("SOMETHING WRONG IN REQUEST DATA", status=status.HTTP_400_BAD_REQUEST)


class ROICalculator(GenericAPIView):
    serializer_class = Transactionserializer
    permission_classes = [AllowAny]

    def __init__(self):
        pass

    def get(self, request, pid):
        if pid == None:
            return Response({"message": "No Portfolio"}, status=status.HTTP_400_BAD_REQUEST)
        ROI = self.calculate(request, pid)
        return Response({"ROI": ROI}, status=status.HTTP_200_OK)

    def calculate(self, request, id=None):
        # step1 get transactions (create portfolio - a week ago) and (a week ago - now)
        # portfolio_now = Portfolio.objects.get(pk=id)
        today = datetime.date.today()
        end_date = datetime.date(today.year, today.month, today.day)
        start_date = end_date - datetime.timedelta(days=7)

        transaction_week = list(
            Transaction.objects.filter(Q(portfolio__id=id) & Q(time__gte=start_date)).order_by("time").values()
        )

        transaction_before_week_ago = list(
            Transaction.objects.filter(Q(portfolio__id=id) & Q(time__lt=start_date)).order_by("time").values()
        )
        # step2 trace back from now to a week ago
        # value = (market value - average cost) + (net cash flow)
        stocks_week_ago = {}
        stocks_now = {}

        for t in transaction_before_week_ago:
            if t["amount"] > 0:
                if stocks_week_ago.get(t["stock_id"]) == None:
                    stocks_week_ago[t["stock_id"]] = {"cost": 0.0, "amount": 0.0}
                old_cost = stocks_week_ago[t["stock_id"]]["cost"] * stocks_week_ago[t["stock_id"]]["amount"]
                new_cost = t["amount"] * t["price"]
                new_amount = stocks_week_ago[t["stock_id"]]["amount"] + t["amount"]
                stocks_week_ago[t["stock_id"]]["cost"] = (old_cost + new_cost) / (new_amount) if new_amount != 0 else 0
                stocks_week_ago[t["stock_id"]]["amount"] = new_amount

        stocks_now = stocks_week_ago
        cash_flow = 0
        total_cost = 0
        for t in transaction_week:
            if stocks_week_ago.get(t["stock_id"]) == None:
                stocks_week_ago[t["stock_id"]] = {"cost": 0.0, "amount": 0.0}
            # sell stock: calculate cash flow and update amount
            if t["amount"] < 0:
                amount = abs(t["amount"])
                total_cost += stocks_now[t["stock_id"]]["cost"] * amount
                cash_flow += (t["price"] - stocks_now[t["stock_id"]]["cost"]) * amount
                stocks_now[t["stock_id"]]["amount"] += t["amount"]
            else:
                # buy stock: calculate average cost
                old_cost = stocks_now[t["stock_id"]]["cost"] * stocks_now[t["stock_id"]]["amount"]
                new_cost = t["amount"] * t["price"]
                new_amount = stocks_now[t["stock_id"]]["amount"] + t["amount"]
                stocks_now[t["stock_id"]]["cost"] = (old_cost + new_cost) / (new_amount) if new_amount != 0 else 0
                stocks_now[t["stock_id"]]["amount"] = new_amount

        # step3 calculate ROI
        net_return = 0
        investment = 0
        for key, value in stocks_now.items():
            if value["amount"] != 0:
                stockprice = list(Stockprice.objects.filter(Q(stock__id=str(key)) & Q(time__day=today.day)).values())

                net_return += (value["cost"] - stockprice[0]["price"]) * value["amount"]
                investment += value["cost"] * value["amount"]

        net_return += cash_flow
        investment += total_cost
        ROI = net_return / investment
        return round(ROI, 4) * 100
