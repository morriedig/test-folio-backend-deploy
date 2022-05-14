from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsUserInfoCompleted(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            user = request.user
            response = {}
            is_done = True
            for field in ["id_number", "username", "bankaccount"]:
                if getattr(user, field) == "":
                    response[field] = f"{field} is empty, please use [PUT / PATCH]/api/user/ to update it"
                    is_done = False

            if is_done:
                return True
            else:
                raise PermissionDenied(detail=response)

        return False
