from django.db import models
from django.utils import timezone
from django.conf import settings

class Project(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=250, unique_for_date='published')

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.content