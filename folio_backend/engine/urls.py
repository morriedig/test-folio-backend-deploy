from django.urls import path

from .follow_views import FollowAPIView
from .transaction_views import ROICalculator, TransactionAPIView

urlpatterns = [
    path("transaction/", TransactionAPIView.as_view()),
    path("follow/", FollowAPIView.as_view()),
    path("ROI/<int:pid>", ROICalculator.as_view()),
]
