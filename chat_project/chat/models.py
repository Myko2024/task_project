from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Thread(models.Model):
    participants = models.ManyToManyField(User, related_name="threads")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.pk and self.participants.count() > 2:
            raise ValidationError(_("A thread cannot have more than 2 participants."))

    def __str__(self):
        participants = self.participants.values_list("username", flat=True)
        return f"Thread between {', '.join(participants)}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    thread = models.ForeignKey(
        Thread, related_name="messages", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} in thread {self.thread.id}"
