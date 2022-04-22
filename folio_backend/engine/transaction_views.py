from datetime import datetime

from engine.models import *
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .transaction_serializers import Transactionserializer


# Create your views here.
class TransactionAPIView(GenericAPIView):
    serializer_class = Transactionserializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **krgs):
        try:
            data = request.data
            stock_code = data["stock"]
            amount = data["cash"]
            pid = data["pid"]

            time = datetime.now()
            stock = Stock.objects.get(code=stock_code)
            price = stock.price
            portfolio = Portfolio.objects.get(id=pid)

            if portfolio.cash <= amount:
                return Response("NOT ENOUGH CASH", status=status.HTTP_402_PAYMENT_REQUIRED)
            new_transaction = Transaction(portfolio=portfolio, stock=stock, amount=amount, time=time, price=price)
            new_transaction.save()

            return Response("SUCCESS", status=status.HTTP_200_OK)
        except:
            return Response("SOMETHING WRONG IN REQUEST DATA", status=status.HTTP_400_BAD_REQUEST)
