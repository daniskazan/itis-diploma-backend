from rest_framework import serializers
from core.models import Resource, Script, CommandParameter


class CommandPatternSerializer(serializers.ModelSerializer):
    class CommandParameterSerializer(serializers.ModelSerializer):
        class Meta:
            model = CommandParameter
            fields = ["name", "description", "field_type", "payload_field"]

    command_parameters = CommandParameterSerializer(many=True)

    class Meta:
        model = Script
        fields = ["id", "command_description", "command_parameters"]


class ResourceSerializer(serializers.ModelSerializer):
    resource_group = serializers.CharField(source="resource_group.name")
    scripts = CommandPatternSerializer(many=True)

    class Meta:
        model = Resource
        exclude = ["resource_url", "created_at", "updated_at"]
