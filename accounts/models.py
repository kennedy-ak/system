from django.db import models
from django.conf import settings


class UserProfile(models.Model):
	"""Simple profile extension for built-in User."""
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	bio = models.TextField(blank=True)
	avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

	def __str__(self):
		return f"Profile: {self.user.username}"
