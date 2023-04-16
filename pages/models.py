from django.db import models
from django.conf import settings
from django.utils import timezone

class Page(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date_published = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    image = models.ImageField(upload_to='pages', default='default.jpg')

    def __str__(self):
        return self.title

    def get_author_name(self):
        return self.author.username