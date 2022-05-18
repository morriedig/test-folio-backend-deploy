from datetime import datetime

from engine.models import Portfolio, Stock, Transaction
from engine.rules import PortfolioCreatePermission, PortfolioRetrievePermission, PortfolioUpdatePermission
from IAM.models import MyUser
from IAM.permissions import IsUserInfoCompleted
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from .serializers import PortfolioSerializer, PublicPortfolioSerializer


# Create your views here.
class PortfolioAPIView(GenericAPIView, ListModelMixin):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = []

    def get_permissions(self):
        if self.request.method in ["POST"]:
            self.permission_classes.append(IsUserInfoCompleted)
            self.permission_classes.append(PortfolioCreatePermission)
        elif self.request.method in ["GET"] and self.request.query_params.get("pid", "") != "":
            self.permission_classes.append(PortfolioRetrievePermission)
        elif self.request.method in ["PATCH"]:
            self.permission_classes.append(IsUserInfoCompleted)
            self.permission_classes.append(PortfolioUpdatePermission)
        return [permission() for permission in self.permission_classes]

    def get(self, request, *args, **kargs):
        pid = request.query_params.get("pid", "")
        # order_by = request.query_params.get("order", "follow")
        try:
            if pid == "":
                portfolio = Portfolio.objects.filter(is_public=True, is_alive=True).all()
            else:
                portfolio = Portfolio.objects.filter(id=pid)
        except:
            return Response(
                "PORTFOLIO " + str(pid) + " DOES NOT EXIST OR DISCARDED OR PRIVATE", status=status.HTTP_400_BAD_REQUEST
            )
        for p in portfolio:
            self.check_object_permissions(self.request, p)
        if isinstance(request.user, MyUser):
            serializer = PortfolioSerializer(portfolio, many=True, context={"user": request.user})
        else:
            serializer = PublicPortfolioSerializer(portfolio, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response("no auth or no profolio", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kargs):
        data = request.data
        if "name" not in data:
            return Response("MISSING name IN REQUEST", status=status.HTTP_400_BAD_REQUEST)
        if "description" not in data:
            return Response("MISSING description IN REQUEST", status=status.HTTP_400_BAD_REQUEST)
        if "follow_price" not in data:
            return Response("MISSING follow_price IN REQUEST", status=status.HTTP_400_BAD_REQUEST)
        if "budget" not in data:
            return Response("MISSING budget IN REQUEST", status=status.HTTP_400_BAD_REQUEST)
        if "is_public" not in data:
            is_public = True
        else:
            is_public = data["public"]

        if request.user.budget < data["budget"]:
            return Response("NOT ENOUGH MONEY TO AFFORD YOUR CASH", status=status.HTTP_402_PAYMENT_REQUIRED)
        request.user.budget -= data["budget"]
        request.user.save()
        new_portfolio = Portfolio(
            name=data["name"],
            description=data["description"],
            owner=request.user,
            follow_price=data["follow_price"],
            budget=data["budget"],
            is_public=is_public,
            is_alive=True,
        )
        new_portfolio.save()
        new_transaction = Transaction(
            portfolio=new_portfolio,
            stock=Stock.objects.get(code="0000"),
            amount=data["budget"],
            time=datetime.now(),
            price=1,
        )
        new_transaction.save()
        return Response("SUCCESS", status=status.HTTP_200_OK)

    def patch(self, request, *args, **kargs):

        data = request.data
        if "pid" not in data:
            return Response("MISSING pid IN REQUEST", status=status.HTTP_400_BAD_REQUEST)
        pid = data["pid"]
        has_name = False
        has_description = False
        has_follow_price = False
        has_is_public = False
        if "name" in data:
            has_name = data["name"]
        if "description" in data:
            has_description = data["description"]
        if "follow_price" in data:
            has_follow_price = data["follow_price"]
        if "is_public" in data:
            has_is_public = data["is_public"]
        try:
            portfolio = Portfolio.objects.get(id=pid)
        except:
            return Response("PORTFOLIO " + str(pid) + " DOES NOT EXIST", status=status.HTTP_400_BAD_REQUEST)
        if request.user != portfolio.owner:
            return Response("YOU CANNOT CHANGE OTHERS PORTFOLIO", status=status.HTTP_403_FORBIDDEN)
        if has_name != False:
            portfolio.name = has_name
        if has_description != False:
            portfolio.description = has_description
        if has_follow_price != False:
            portfolio.follow_price = has_follow_price
        if has_is_public != False:
            portfolio.is_public = has_is_public
        portfolio.save()
        return Response("SUCCESS", status=status.HTTP_200_OK)
