from engine.models import Stock
from rest_framework import serializers


class Stockserializer(serializers.ModelSerializer):

    # price = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     read_only=True,
    #   )
    # price = price.data

    class Meta:
        model = Stock
        fields = ("code", "name", "last_price", "last_day_change")
