from django.db import models
from account.models import Account

class Message(models.Model):
    sender = models.ForeignKey(Account, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Account, related_name='receiver', on_delete=models.CASCADE)
    content = models.TextField()
    issue_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sender)
