import json

from django.core.serializers import serialize
from rest_framework.serializers import CharField, ValidationError

from .models import Portfolio


class GetAllPortfolioSerializer:
    class Meta:
        model = Portfolio
        fields = ["name", "description", "owner", "cash", "budget", "is_public", "is_alive"]

    def get_all(self):
        return serialize(
            "json",
            Portfolio.objects.all(),
            fields=("name", "description", "owner", "cash", "budget", "is_public", "is_alive"),
        )

    def get_specific(self, id):
        specific = Portfolio.objects.get(pk=id)
        d = {"portfolio_name": specific.name, "stocks": specific.stocks}
        return json.dumps(d, ensure_ascii=False)


class PasswordChangeSerializer:
    current_password = CharField(style={"input_type": "password"}, required=True)
    new_password = CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise ValidationError({"current_password": "Does not match"})
        return value
