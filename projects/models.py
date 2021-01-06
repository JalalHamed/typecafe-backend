from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=250, unique_for_date='published')

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.content