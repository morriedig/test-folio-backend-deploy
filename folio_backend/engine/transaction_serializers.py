from engine.models import Transaction
from rest_framework import serializers


class Transactionserializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
