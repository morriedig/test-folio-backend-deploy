from cmath import exp
from datetime import datetime

from engine.models import *
from IAM.models import MyUser
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import PortfolioDetailSerializer, PortfolioSerializer


# Create your views here.
class PortfolioAPIView(GenericAPIView, ListModelMixin):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kargs):
        try:
            return self.list(request, *args, **kargs)
        except:
            return Response("no auth or no profolio", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kargs):
        # try:
        data = request.data

        new_portfolio = Portfolio(
            name=data["name"],
            description=data["description"],
            cash=data["cash"],
            stocks=data["stocks"],
            follow_price=data["follow_price"],
            budget=data["budget"],
            is_public=data["is_public"],
            is_alive=data["is_alive"],
            owner=MyUser.objects.get(pk=int(data["owner"]))
            # owner=data["owner"],
        )
        new_portfolio.save()
        return Response("SUCCESS", status=status.HTTP_200_OK)

    # except:
    #     return Response("no auth", status=status.HTTP_400_BAD_REQUEST)


class PortfolioAPIDetailView(GenericAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioDetailSerializer
    lookup_field = "ID"
    # permission_classes = [IsAuthenticated]
    def get_object(self, ID):
        try:
            return Portfolio.objects.get(pk=ID)
        except Portfolio.DoesNotExist:
            return None

    def get(self, request, ID, *args, **kargs):
        try:
            instance = self.get_object(ID)
            serializer = PortfolioDetailSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("no auth or no profolio", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, ID, *args, **kwargs):
        instance = self.get_object(ID)
        data = request.data
        serializer = PortfolioDetailSerializer(instance=instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # # try:
        # instance = self.get_object(ID)
        # instance.name = request.data.get("name")
        # instance.save()

        # serializer = self.get_serializer(instance)
        # serializer.is_valid()
        # self.perform_update(serializer)

        # return Response(serializer.data)

    # except:
    #     return Response("no auth or no profolio", status=status.HTTP_400_BAD_REQUEST)


# class PortfolioOperationsHandler:
#     def __init__(self):
#         self.serializer = GetAllPortfolioSerializer()

#     def router_(self, request, id=None):
#         # print(request)
#         if request.method == "GET" and id == None:
#             return self.get_all_portfolio()
#         elif request.method == "GET" and id != None:
#             return self.get_specific_portfolio(id)
#         elif request.method == "POST" and id == None:
#             return self.create_portfolio(request)
#         elif request.method == "POST" and id != None:
#             return self.update_portfolio(id)

#     def get_all_portfolio(self):
#         try:
#             portfolios = self.serializer.get_all()
#             return HttpResponse(portfolios, status=status.HTTP_200_OK)
#         except:
#             return HttpResponse({"message": "No auth or no profolio"}, status=status.HTTP_400_BAD_REQUEST)

#     def get_specific_portfolio(self, id):
#         try:
#             portfolio = self.serializer.get_specific(id)
#             return HttpResponse(portfolio, status=status.HTTP_200_OK)
#         except:
#             return HttpResponse({"message": "no auth or no profolio, please login"}, status=status.HTTP_400_BAD_REQUEST)

#     def create_portfolio(self, request):

#         Portfolio.objects.create(
#             name=request.POST["name"],
#             description=request.POST["description"],
#             owner=request.POST["owner"],
#             cash=request.POST["cash"],
#             budget=request.POST["budget"],
#         )

#     def update_portfolio(self, request, id):
#         Portfolio.objects.update()
#         p = Portfolio.objects.get(pk=id)
#         p.name = request.POST["name"]
#         p.is_public = request.POST["is_public"]
#         p.description = request.POST["description"]
#         p.budget = request.POST["budget"]
#         p.save()
