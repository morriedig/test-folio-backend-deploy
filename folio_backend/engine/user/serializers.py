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
    class Meta:
        model = MyUser
        fields = ("id", "account", "email", "id_number", "username", "bankaccount", "budget", "picture")


class UserSpecificRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id", "account", "email", "id_number", "username")
