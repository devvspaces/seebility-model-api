from rest_framework import serializers
from chat.models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = "__all__"
        read_only_fields = ("room_name", "ai", "message", "created_at")


class SpeechToTextSerializer(serializers.Serializer):
    record = serializers.CharField()


class SpeechToTextPresenter(serializers.Serializer):
    text = serializers.CharField()
