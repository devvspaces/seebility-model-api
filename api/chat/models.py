from django.db import models

# NOTE: Indexed room_name for faster lookup


class ChatMessage(models.Model):
    room_name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ai = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        indexes = [
            models.Index(fields=["room_name"], name="room_name_idx"),
        ]
