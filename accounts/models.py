from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from PIL import Image


def validate_image(image):
	"""Validate image quality and format - only reject truly unusable images"""
	try:
		# Open the image to verify it's valid
		img = Image.open(image)
		img.verify()

		# Re-open for further checks (verify() closes the file)
		image.seek(0)
		img = Image.open(image)

		# Only reject if image is extremely small (likely corrupt or placeholder)
		width, height = img.size
		if width < 50 or height < 50:
			raise ValidationError('Image is too small. Minimum size is 50x50 pixels.')

		# Check file size - only reject extremely large files (>10MB)
		if image.size > 10 * 1024 * 1024:
			raise ValidationError('Image file size cannot exceed 10MB.')

		# Accept all common formats
		valid_formats = ['JPEG', 'JPG', 'PNG', 'GIF', 'BMP', 'WEBP']
		if img.format not in valid_formats:
			raise ValidationError(f'Unsupported image format. Accepted formats: {", ".join(valid_formats)}')

	except ValidationError:
		raise
	except Exception as e:
		# Only raise error for truly unusable images
		raise ValidationError(f'Invalid or corrupted image file: {str(e)}')


class UserProfile(models.Model):
	"""Simple profile extension for built-in User."""
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	bio = models.TextField(blank=True)
	avatar = models.ImageField(
		upload_to='avatars/',
		null=True,
		blank=True,
		validators=[validate_image],
		help_text='Upload a profile picture (JPEG, PNG, GIF, BMP, WEBP). Minimum 50x50px, maximum 10MB.'
	)

	def __str__(self):
		return f"Profile: {self.user.username}"
