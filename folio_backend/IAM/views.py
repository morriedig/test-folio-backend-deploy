from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PasswordChangeSerializer, RegistrationSerializer
from .utils import get_tokens_for_user

# Create your views here.


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        if "account" not in request.data or "password" not in request.data:
            return Response({"message": "Credentials missing"}, status=status.HTTP_400_BAD_REQUEST)
        account = request.POST["account"]
        password = request.POST["password"]
        user = authenticate(request, account=account, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            print(user)
            return Response(
                {"message": "Login Success", "id": user.id, "account": user.account, **auth_data},
                status=status.HTTP_200_OK,
            )
        return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={"request": request}, data=request.data)
        serializer.is_valid(raise_exception=True)  # Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response(
            {"message": "Successfully changed password, please login again."}, status=status.HTTP_204_NO_CONTENT
        )
