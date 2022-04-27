from django.urls import path

from .transaction_views import ROICalculator

urlpatterns = [path("ROI/<int:pid>", ROICalculator.as_view())]
