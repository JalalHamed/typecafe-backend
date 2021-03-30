from django.db import models
from account.models import Account

def upload_path(instance, filename):
    return '/'.join(['projects', filename])


class Project(models.Model):
    STATUS_CHOICES = [
        ('O', 'Open'),
        ('IP', 'In Progress'),
        ('D', 'Done'),
        ('J', 'Judgment'),
    ]

    client = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=upload_path)
    languages_and_additions = models.TextField()
    number_of_pages = models.IntegerField()
    delivery_deadline = models.IntegerField()
    description = models.TextField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='O')

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.description
