from datetime import datetime

from engine.models import *
from IAM.models import MyUser
from IAM.permissions import IsUserInfoCompleted
from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSelfRetrieveSerializer, UserSpecificRetrieveSerializer, UserUpdateSerializer


class UserSelfView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericAPIView):

    queryset = MyUser.objects.all()
    permission_classes = [IsAuthenticated]

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
    serializer_class = UserSpecificRetrieveSerializer
    queryset = MyUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response = Response({"message": "success", "data": response.data})
        return response
