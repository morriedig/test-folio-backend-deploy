from django.urls import path

from .follow_views import FollowAPIView
from .stock_views import StockAPIView
from .transaction_views import TransactionAPIView

urlpatterns = [
    path("transaction/", TransactionAPIView.as_view()),
    path("follow/", FollowAPIView.as_view()),
    path("stock/", StockAPIView.as_view()),
]
