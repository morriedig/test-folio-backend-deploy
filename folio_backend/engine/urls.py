from django.urls import path

from .transaction_views import TransactionAPIView

urlpatterns = [
    path("transaction/", TransactionAPIView.as_view()),
]
