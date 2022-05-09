# from .utils import *

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .stock_serializers import Stockserializer


# Create your views here.
class StockAPIView(GenericAPIView):
    serializer_class = Stockserializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **krgs):
        try:
            code = request.query_params.get("code", "")
            name = request.query_params.get("name", "")
            if code != "":
                stock = Stock.objects.filter(code__startswith=code)
            elif name != "":
                stock = Stock.objects.filter(name__startswith=name)
            else:
                return Response("NO NAME OR CODE IN REQUEST DATA", status=status.HTTP_400_BAD_REQUEST)
            serializer = Stockserializer(stock, many=True)

            return Response(serializer.data)
        except:
            return Response("Maybe somthing WRONG IN REQUEST DATA", status=status.HTTP_400_BAD_REQUEST)
