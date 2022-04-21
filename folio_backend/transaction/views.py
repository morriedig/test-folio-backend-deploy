from datetime import datetime

from engine.models import *
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import Transactionserializer


# Create your views here.
class Transaction(GenericAPIView):
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

            new_transaction = Transaction(portfolio=portfolio, stock=stock, amount=amount, time=time, price=price)
            new_transaction.save()

            return Response("success")
        except:
            return Response("what's wrong with you")
