from engine.models import Portfolio
from IAM.models import MyUser
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import PortfolioDetailSerializer, PortfolioSerializer


# Create your views here.
class PortfolioAPIView(GenericAPIView, ListModelMixin):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]

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
            owner=MyUser.objects.get(pk=int(data["owner"])),
        )
        new_portfolio.save()
        return Response("SUCCESS", status=status.HTTP_200_OK)


class PortfolioAPIDetailView(GenericAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioDetailSerializer
    lookup_field = "ID"
    permission_classes = [IsAuthenticated]

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
