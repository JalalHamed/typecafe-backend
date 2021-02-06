from django.db import models

def upload_path(instance, filename):
    # return '/'.join(['projects', str(instance.client), filename])
    return '/'.join(['projects', filename])


class Project(models.Model):
    STATUS_CHOICES = [
        ('OP', 'Open'),
        ('IP', 'In Progress'),
        ('DN', 'Done'),
        ('JM', 'Judgment'),
    ]

    # client = models.CharField(max_length=50)
    # typist = models.CharField(max_length=50)
    files = models.FileField(upload_to=upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    # deadline = models.TimeField()
    description = models.TextField()
    # number_of_pages = models.IntegerField()
    # price_per_page = models.IntegerField()
    # total_price = models.IntegerField()
    # guarantee_price = models.IntegerField()
    # views = models.IntegerField(default=0)
    # status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='OP'),
    
    def __str__(self):
        return self.description