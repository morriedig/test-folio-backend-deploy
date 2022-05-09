from django.urls import path

from .follow_views import FollowAPIView
from .transaction_views import ROICalculator, TransactionAPIView
from .user.views import UserSelfView, UserSpecificView
from .stock_views import StockAPIView

urlpatterns = [
    path("transaction/", TransactionAPIView.as_view()),
    path("follow/", FollowAPIView.as_view()),
    path("stock/", StockAPIView.as_view()),
    path("user/", UserSelfView.as_view()),
    path("user/<int:pk>/", UserSpecificView.as_view()),
    path("ROI/<int:pid>", ROICalculator.as_view()),
]
