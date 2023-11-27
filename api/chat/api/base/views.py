from uuid import uuid4
from utils.auth import IsAuthorized, IsValidApiKey
from chat.models import ChatMessage
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from . import serializers
from llm.utils import stt
import base64
from django.conf import settings
import os


class GetChatsView(generics.ListAPIView):
    serializer_class = serializers.ChatMessageSerializer
    # permission_classes = [IsValidApiKey, IsAuthorized]

    def get_queryset(self):
        # return ChatMessage.objects.filter(
        #     room_name=self.request.user_id)
        return ChatMessage.objects.filter(
            room_name=self.kwargs["user_id"])


class SpeechToTextView(generics.GenericAPIView):
    serializer_class = serializers.SpeechToTextPresenter
    permission_classes = [IsValidApiKey, IsAuthorized]

    @swagger_auto_schema(
        responses={200: serializers.SpeechToTextPresenter},
        request_body=serializers.SpeechToTextSerializer(),
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.SpeechToTextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        audio = serializer.validated_data["record"]
        audio = base64.b64decode(audio)
        audio_path = settings.BASE_DIR / f'{uuid4()}.wav'
        with open(audio_path, "wb") as audio_f:
            audio_f.write(audio)
        with open(audio_path, "rb") as audio_r:
            text = stt(audio_r)
            os.remove(audio_path)
            return Response(
                {"text": text}, status=status.HTTP_200_OK
            )
