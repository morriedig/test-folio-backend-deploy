from IAM.models import MyUser
from rest_framework import serializers


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            "id",
            "email",
            "id_number",
            "username",
            "bankaccount",
            "picture",
        )
        read_only_fields = ("id",)

    # TODO: validate data, e.g., uniqueness
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.owner_id = validated_data.get('owner_id', instance.owner_id)
    #     instance.assignee_id = validated_data.get('assignee_id', instance.assignee_id)
    #     instance.bug_tracker = validated_data.get('bug_tracker', instance.bug_tracker)
    #     labels = validated_data.get('label_set', [])
    #     for label in labels:
    #         LabelSerializer.update_instance(label, instance)

    #     instance.save()
    #     return instance

    # def validate_labels(self, value):
    #     if value:
    #         label_names = [label['name'] for label in value]
    #         if len(label_names) != len(set(label_names)):
    #             raise serializers.ValidationError('All label names must be unique for the project')
    #     return value


class UserSelfRetrieveSerializer(serializers.ModelSerializer):
    num_follower = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ("id", "account", "email", "id_number", "username", "bankaccount", "budget", "num_follower", "picture")

    def get_num_follower(self, obj):
        return get_user_num_follower(obj)


class UserSpecificRetrieveSerializer(serializers.ModelSerializer):
    num_follower = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ("id", "account", "email", "username", "num_follower")

    def get_num_follower(self, obj):
        return get_user_num_follower(obj)


class PublicUserSpecificRetrieveSerializer(serializers.ModelSerializer):
    num_follower = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ("id", "account", "num_follower")

    def get_num_follower(self, obj):
        return get_user_num_follower(obj)


class UserAddValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id", "account", "budget")
        read_only_fields = ("id", "account", "budget")


def get_user_num_follower(user):
    return sum([p.num_follower for p in user.portfolio_set.all().filter(is_alive=True)])
