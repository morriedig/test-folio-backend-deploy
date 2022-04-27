from engine.models import Transaction
from rest_framework import serializers


class Transactionserializer(serializers.ModelSerializer):
    # days_since_created = serializers.SerializerMethodField()
    # singer = ToUpperCaseCharField()

    class Meta:
        model = Transaction
        fields = "__all__"

    # def get_sth_new_to_calculate(self, objd):
    #     pass
