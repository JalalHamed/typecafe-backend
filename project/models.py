from django.db import models
from account.models import Account

def upload_path(instance, filename):
    return '/'.join(['projects', filename])


class Project(models.Model):
    STATUS_CHOICES = [
        ('OP', 'Open'),
        ('IP', 'In Progress'),
        ('DN', 'Done'),
        ('JM', 'Judgment'),
    ]

    client = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to=upload_path)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='OP')

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.description
