from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status

from .models import Portfolio
from .serializer import GetAllPortfolioSerializer

# Create your views here.


class PortfolioOperationsHandler:
    def __init__(self):
        self.serializer = GetAllPortfolioSerializer()

    def router_(self, request, id=None):
        # print(request)
        if request.method == "GET" and id == None:
            return self.get_all_portfolio()
        elif request.method == "GET" and id != None:
            return self.get_specific_portfolio(id)
        elif request.method == "POST" and id == None:
            return self.create_portfolio(request)
        elif request.method == "POST" and id != None:
            return self.update_portfolio(id)

    def get_all_portfolio(self):
        try:
            portfolios = self.serializer.get_all()
            return HttpResponse(portfolios, status=status.HTTP_200_OK)
        except:
            return HttpResponse({"message": "No auth or no profolio"}, status=status.HTTP_400_BAD_REQUEST)

    def get_specific_portfolio(self, id):
        try:
            portfolio = self.serializer.get_specific(id)
            return HttpResponse(portfolio, status=status.HTTP_200_OK)
        except:
            return HttpResponse({"message": "no auth or no profolio, please login"}, status=status.HTTP_400_BAD_REQUEST)

    def create_portfolio(self, request):

        Portfolio.objects.create(
            name=request.POST["name"],
            description=request.POST["description"],
            owner=request.POST["owner"],
            cash=request.POST["cash"],
            budget=request.POST["budget"],
        )

    def update_portfolio(self, request, id):
        Portfolio.objects.update()
        p = Portfolio.objects.get(pk=id)
        p.name = request.POST["name"]
        p.is_public = request.POST["is_public"]
        p.description = request.POST["description"]
        p.budget = request.POST["budget"]
        p.save()
