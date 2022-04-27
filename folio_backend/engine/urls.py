from django.urls import path

from .follow_views import FollowAPIView
from .portfolio.views import PortfolioAPIDetailView, PortfolioAPIView
from .transaction_views import TransactionAPIView

urlpatterns = [
    path("transaction/", TransactionAPIView.as_view()),
    path("follow/", FollowAPIView.as_view()),
    path("portfolio/", PortfolioAPIView.as_view()),
    path("portfolio/<int:ID>/", PortfolioAPIDetailView.as_view()),
]
