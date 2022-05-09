from datetime import datetime

from django.db.models import Sum
from engine.models import *
from IAM.models import *

# from IAM.permissions import IsUserInfoCompleted
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .follow_serializers import Followserializer

# from .utils import *


# Create your views here.
class FollowAPIView(GenericAPIView):
    serializer_class = Followserializer
    # permission_classes = [IsUserInfoCompleted]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **krgs):
        try:
            user = request.user
            # uid = request.query_params.get("user", "")
            # user = MyUser.objects.get(id=uid)
            pid = request.query_params.get("pid", "")
            if pid != "":
                if user != Portfolio.objects.get(id=pid).owner:
                    return Response("Not the owner", status=status.HTTP_401_UNAUTHORIZED)
                else:
                    portfolio = Portfolio.objects.get(id=pid)
                    follow = Follow.objects.filter(portfolio=portfolio)
                    serializer = Followserializer(follow, many=True)
                    return Response(serializer.data)
            follow = Follow.objects.filter(user=user)
            serializer = Followserializer(follow, many=True)
            return Response(serializer.data)
        except:
            return Response("Maybe somthing WRONG IN REQUEST DATA", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **krgs):
        try:
            data = request.data
            user = request.user
            if data["is_follow"] == 1:
                cash = float(data["cash"])
                pid = data["pid"]
                portfolio = Portfolio.objects.get(id=pid)
                follow = Follow.objects.filter(portfolio=portfolio, user=user, is_alive=True)
                if len(follow) != 0:
                    return Response("Have Followed", status=status.HTTP_409_CONFLICT)
                if user.budget < portfolio.follow_price + cash:
                    return Response("NOT ENOUGH BUDGET", status=status.HTTP_402_PAYMENT_REQUIRED)
                new_follow = Follow(
                    portfolio=portfolio,
                    user=user,
                    starttime=datetime.now(),
                    budget=cash,
                )
                new_follow.save()
                owner = portfolio.owner
                target_user = MyUser.objects.filter(id=user.id)
                target_owner = MyUser.objects.filter(id=owner.id)
                target_user.update(budget=user.budget - portfolio.follow_price - cash)
                target_owner.update(budget=owner.budget + portfolio.follow_price)
                return Response("SUCCESS", status=status.HTTP_200_OK)
            elif data["is_follow"] == 0:
                money = 0.0
                pid = data["pid"]
                portfolio = Portfolio.objects.get(id=pid)
                follow = Follow.objects.filter(portfolio=portfolio, user=user, is_alive=True)
                transaction = (
                    Transaction.objects.filter(portfolio=portfolio).values("stock").annotate(total_amount=Sum("amount"))
                )
                for stock in transaction:
                    stockprice = Stockprice.objects.filter(stock=stock["stock"]).order_by("-time")[0]
                    message += str(stock)
                    message += ", "
                    message += str(stock["total_amount"])
                    message += ", "
                    message += str(stockprice.price)
                    message += ", "
                    money += stock["total_amount"] * stockprice.price

                money = money / portfolio.budget * follow[0].budget
                target_user = MyUser.objects.filter(id=user.id)
                target_user.update(budget=user.budget + money)
                follow.update(is_alive=False)
                return Response("UNFOLLOW SUCCESS", status=status.HTTP_200_OK)

            return Response("SUCCESS", status=status.HTTP_200_OK)
        except:
            return Response("Maybe somthing WRONG IN REQUEST DATA", status=status.HTTP_400_BAD_REQUEST)
