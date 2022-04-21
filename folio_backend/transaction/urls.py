from django.urls import path

from . import views

urlpatterns = [path("", views.Transaction.as_view())]
