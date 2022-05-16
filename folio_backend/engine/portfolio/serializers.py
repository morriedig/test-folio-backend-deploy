from engine.models import Follow, Portfolio
from engine.utils import getROI
from rest_framework import serializers


class PortfolioSerializer(serializers.ModelSerializer):
    num_of_follower = serializers.SerializerMethodField("calculateFollower")
    owner_account = serializers.SerializerMethodField("getOwnerName")
    roi = serializers.SerializerMethodField("getROI")
    is_follow = serializers.SerializerMethodField("getIsFollow")
    is_owner = serializers.SerializerMethodField("getIsOwner")

    def calculateFollower(self, portfolio):
        return Follow.objects.filter(portfolio=portfolio, is_alive=False).count()

    def getOwnerName(self, portfolio):
        return portfolio.owner.account

    def getROI(self, portfolio):
        ROI = getROI(portfolio.id, 1)
        return ROI

    def getIsFollow(self, portfolio):
        user = self.context["user"]
        return Follow.objects.filter(portfolio=portfolio, user=user, is_alive=True).count() > 0

    def getIsOwner(self, portfolio):
        user = self.context["user"]
        return portfolio.owner == user

    class Meta:
        model = Portfolio
        fields = ("name", "owner_account", "num_of_follower", "roi", "is_follow", "is_owner")
        # ordering = ["num_of_follower", "roi"]
