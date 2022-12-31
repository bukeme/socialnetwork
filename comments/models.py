from django.db import models
from django.conf import settings
from django.urls import reverse
from posts.models import Post 

User = settings.AUTH_USER_MODEL

# Create your models here.

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.content[:50]

	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'pk': self.post.pk})

	class Meta:
		ordering = ['-created']

