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
    type = models.TextField()
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default='O')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)


class Offer(models.Model):
    STATUS_CHOICES = [
        ('A', 'Await'),
        ('ACC', 'Accepted'),
        ('REJ', 'Rejected'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    typist = models.ForeignKey(Account, on_delete=models.CASCADE)
    offered_price = models.IntegerField()
    status = models.CharField(
        max_length=3, choices=STATUS_CHOICES, default='A')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)
