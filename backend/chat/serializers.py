from rest_framework import serializers
from .models import Session, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'created_at']


class SessionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    legend_id = serializers.CharField(read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'legend_id', 'lang', 'created_at', 'messages']


class StartSessionSerializer(serializers.Serializer):
    legend_id = serializers.CharField()
    lang = serializers.CharField(required=False)


class SendMessageSerializer(serializers.Serializer):
    content = serializers.CharField()
    llm_url = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    llm_model = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    llm_api_key = serializers.CharField(required=False, allow_blank=True, allow_null=True)