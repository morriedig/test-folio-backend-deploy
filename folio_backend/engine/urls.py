from django.urls import path

from .follow_views import FollowAPIView
from .transaction_views import TransactionAPIView
from .user.views import UserSelfView, UserSpecificView

urlpatterns = [
    path("transaction/", TransactionAPIView.as_view()),
    path("follow/", FollowAPIView.as_view()),
    path("user/", UserSelfView.as_view()),
    path("user/<int:pk>/", UserSpecificView.as_view()),
]
