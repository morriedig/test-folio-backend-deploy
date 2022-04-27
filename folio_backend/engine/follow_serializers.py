from engine.models import Follow
from rest_framework import serializers


class Followserializer(serializers.ModelSerializer):
    # days_since_created = serializers.SerializerMethodField()
    # singer = ToUpperCaseCharField()
    class Meta:
        model = Follow
        fields = "__all__"
