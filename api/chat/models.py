from django.db import models


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


class CartItem(models.Model):
    id = models.CharField(unique=True, primary_key=True)
    user_id = models.CharField(max_length=100, db_column="userId")
    product_id = models.CharField(max_length=100, db_column="productId")
    quantity = models.IntegerField()
    price = models.FloatField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "cart_items"
