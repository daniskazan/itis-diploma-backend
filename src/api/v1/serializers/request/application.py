from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import status
from api.v1.serializers.response.user import ConfirmApplicationByUserSerializer
from core.models import User, Application


class CreateApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Application
        fields = ["user", "resource", "payload", "script"]

    def validate(self, attrs):
        if Application.objects.filter(
            user=attrs["user"], resource=attrs["resource"]
        ).exists():
            raise ValidationError(
                detail="Вы уже подавали заявку", code=status.HTTP_400_BAD_REQUEST
            )
        if not self.context["request"].user.team:
            raise ValidationError(
                detail="Вы не прикреплены к команде. Обратитесь к тимлиду.",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return attrs

    def fetch_team_lead(self) -> User:
        user = self.context["request"].user
        return user.team.team_lead

    def create(self, validated_data: dict) -> Application:
        validated_data.update({"confirm_by": self.fetch_team_lead()})
        return super(CreateApplicationSerializer, self).create(validated_data)


class FullApplicationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.full_name")
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    resource = serializers.ReadOnlyField(source="resource.name")
    status = serializers.CharField(source="get_status_display")
    script = serializers.ReadOnlyField(source="script.command_description")
    confirm_by = ConfirmApplicationByUserSerializer()

    class Meta:
        model = Application
        fields = "__all__"
