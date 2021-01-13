from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(User, null=False, blank=True, default=None, on_delete=models.CASCADE, related_name="users_massage")
    from_user = models.ForeignKey(User, null=False, blank=True, default=None, on_delete=models.CASCADE, related_name="from_user")
    text_message = models.TextField(blank=True, default=None, null=False)
    created = models.DateTimeField(default=datetime.today())

    def __str__(self):
        return f"{self.user} from  {self.from_user}"

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"


class BlackList(models.Model):
    user = models.ForeignKey(User, null=False, blank=True, default=None, on_delete=models.CASCADE, related_name="users_blacklist")
    blocked_user = models.ForeignKey(User, null=False, blank=True, default=None, on_delete=models.CASCADE, related_name="blocked_user")
    created = models.DateTimeField(default=datetime.today())

    def __str__(self):
        return f"{self.user} block {self.blocked_user}"

    class Meta:
        verbose_name = "Black list"
        verbose_name_plural = "Black lists"
