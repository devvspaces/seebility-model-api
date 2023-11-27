from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("chats/<str:user_id>/", views.GetChatsView.as_view(), name="chats"),
    path("speech-to-text/",
         views.SpeechToTextView.as_view(), name="speech-to-text"),
]
