from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from engine import rules
from IAM.models import MyUser
from IAM.permissions import IsUserInfoCompleted
from rest_framework import mixins, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    PublicUserSpecificRetrieveSerializer,
    UserAddValueSerializer,
    UserSelfRetrieveSerializer,
    UserSpecificRetrieveSerializer,
    UserUpdateSerializer,
)


class UserSelfView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericAPIView):

    queryset = MyUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["POST"]:
            self.permission_classes.append(rules.UserCreatePermission)
        elif self.request.method in ["GET"]:
            self.permission_classes.append(rules.UserRetrievePermission)
        elif self.request.method in ["PUT", "PATCH"]:
            self.permission_classes.append(rules.UserUpdatePermission)
        elif self.request.method in ["DELETE"]:
            self.permission_classes.append(rules.UserDeletePermission)

        return [permission() for permission in self.permission_classes]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return UserSelfRetrieveSerializer
        elif self.request.method == "PUT":
            return UserUpdateSerializer
        elif self.request.method == "PATCH":
            return UserUpdateSerializer

    def get(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response = Response({"message": "success", "data": response.data})
        return response

    def put(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response = Response({"message": "success", "data": response.data})
        return response

    def patch(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response = Response({"message": "success", "data": response.data})
        return response


class UserSpecificView(mixins.RetrieveModelMixin, GenericAPIView):
    queryset = MyUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["GET"]:
            if self.request.query_params.get("public") == "true":
                return []

            self.permission_classes.append(rules.UserRetrievePermission)

        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            if self.request.query_params.get("public") == "true":
                return PublicUserSpecificRetrieveSerializer
            else:
                return UserSpecificRetrieveSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "public", openapi.IN_QUERY, description="retrieve public user information", type=openapi.TYPE_BOOLEAN
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response = Response({"message": "success", "data": response.data})
        return response


class UserAddValueView(GenericAPIView):
    permission_classes = [IsUserInfoCompleted]
    serializer_class = UserAddValueSerializer

    def post(self, request, *args, **kwargs):
        if "value" in request.data:
            try:
                v = float(request.data["value"])
            except:
                raise serializers.ValidationError('"value" must be numbers.')

            request.user.budget += v
            request.user.save()
        else:
            raise serializers.ValidationError('"value" field is required.')

        r = self.serializer_class(request.user).data
        response = Response({"message": "success", "data": r})
        return response
