from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from engine.views_test import *
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Folio API",
        default_version="v1",
        description="""
        This service is under development.

        For JWT authorization, please click the Authorize button and fill the value: Bearer <your access token>
        """,
        terms_of_service="http://code.cupidhuang.com/cu2189191862/folio-backend",
        contact=openapi.Contact(email="contact@folio.tw"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("IAM.urls")),
]

# Swagger API document
urlpatterns += [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("insert_test_data/", insert_test_data),
    path("insert_stock/", insert_stock),
    path("insert_stock_price/", insert_stock_price),
    path("insert_test_stock_price/", insert_test_stock_price),
    path("api/", include("engine.urls")),
]
