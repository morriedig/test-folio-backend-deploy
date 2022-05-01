from django.conf import settings
from django.contrib.auth import authenticate
from django.middleware import csrf
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .jwt_integration_view import DecoratedTokenRefreshView
from .serializers import CookieTokenRefreshSerializer, PasswordChangeSerializer, RegistrationSerializer
from .utils import get_tokens_for_user


class RegistrationView(APIView):
    @swagger_auto_schema(
        tags=["auth"],
        request_body=RegistrationSerializer,
        responses={
            201: openapi.Response(
                description="Register a new user.",
                examples={
                    "application/json": {
                        "message": "Register Successfully",
                        "account": "test",
                        "id": "0",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90oxNjQ5Nzg",
                    }
                },
            ),
            400: "Bad Request",
        },
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            # Login after register
            account = request.data["account"]
            password = request.data["password"]
            user = authenticate(request, account=account, password=password)
            response = Response()
            if user is not None:
                if user.is_active:
                    auth_data = get_tokens_for_user(user)
                    response.set_cookie(
                        key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                        value=auth_data["refresh"],
                        expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                        httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                    )
                    csrf.get_token(request)
                    response.data = {
                        "message": "Register Successfully",
                        "id": user.id,
                        "account": user.account,
                        "access": auth_data["access"],
                    }
                    response.status_code = status.HTTP_201_CREATED
                    return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        tags=["auth"],
        operation_description="Check the credentials and return the access token and \
            refresh token will be set in the cookie",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "account": openapi.Schema(type=openapi.TYPE_STRING, description="User's account"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="User's password"),
            },
        ),
        responses={
            200: openapi.Response(
                description="Login.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "id": openapi.Schema(type=openapi.TYPE_STRING),
                        "account": openapi.Schema(type=openapi.TYPE_STRING),
                        "access": openapi.Schema(type=openapi.TYPE_STRING, description="User's JWT access token"),
                    },
                ),
                examples={
                    "application/json": {
                        "message": "Login Successfully",
                        "id": "2",
                        "account": "test",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90oxNjQ5Nzg",
                    }
                },
            ),
            400: openapi.Response(
                description="",
                examples={
                    "application/json": {
                        "message": "This account is not active!",
                    }
                },
            ),
            404: openapi.Response(
                description="",
                examples={
                    "application/json": {
                        "message": "Invalid account or password",
                    }
                },
            ),
        },
    )
    def post(self, request):
        if "account" not in request.data or "password" not in request.data:
            return Response({"message": "Credentials missing"}, status=status.HTTP_400_BAD_REQUEST)
        account = request.data["account"]
        password = request.data["password"]
        user = authenticate(request, account=account, password=password)
        response = Response()
        if user is not None:
            if user.is_active:
                auth_data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=auth_data["refresh"],
                    expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                csrf.get_token(request)
                response.data = {
                    "message": "Login Successfully",
                    "id": user.id,
                    "account": user.account,
                    "access": auth_data["access"],
                }
                response.status_code = status.HTTP_200_OK
                return response
            else:
                return Response({"message": "This account is not active!"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Invalid account or password"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=["auth"],
        operation_description="Logout from the server and delete the corresponding refresh token.",
        responses={
            204: openapi.Response(
                description="Logout successfully.",
                examples={
                    "application/json": {
                        "message": "Logout successfully.",
                    }
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        if self.request.data.get("all"):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"message": "Logout successfully. All refresh tokens blacklisted."})

        # Once logout, then current refresh token in the cookie will be blocked. Thus, one can't use them to obtain access token.
        refresh_token = self.request.COOKIES.get("refresh_token")
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"message": "Logout successfully"}, status=status.HTTP_204_NO_CONTENT)


# TODO: auto-logout in jwt (difficult, since jwt is stateless)
class ChangePasswordView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = PasswordChangeSerializer

    @swagger_auto_schema(
        tags=["auth"],
        operation_description="Change user's password",
        request_body=PasswordChangeSerializer,
        responses={
            204: openapi.Response(
                description="return registraion information without password",
            ),
        },
    )
    def post(self, request):
        serializer = PasswordChangeSerializer(context={"request": request}, data=request.data)
        serializer.is_valid(raise_exception=True)  # Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CookieTokenRefreshView(DecoratedTokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                key="refresh_token",
                value=response.data["refresh"],
                expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                max_age=settings.SIMPLE_JWT["AUTH_COOKIE_MAX_AGE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            del response.data["refresh"]
            access_token_obj = AccessToken(response.data["access"])
            user_id = access_token_obj["user_id"]
            response.data["id"] = user_id

        return super().finalize_response(request, response, *args, **kwargs)
