from django.db import models
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL

# Create your models here.

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	likes = models.ManyToManyField(User, related_name='post_likes')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.content[:50]

	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['-created',]
