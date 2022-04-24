import os

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver



# Create your models here.

def user_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<name>/<filename>
	return '/'.join(['content', instance.user.username, filename])


class uploadFile(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	file_field = models.FileField(upload_to=user_directory_path)
	date_created = models.DateTimeField(auto_now_add=True)

	def filename(self):
		return os.path.basename(self.file.name)

	def __str__(self):
		return f'{self.user}=> {self.file_field}'

	def get_absolute_url(self):
		return reverse('dashboard')


@receiver(models.signals.post_delete, sender=uploadFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
	"""
	Deletes file from filesystem
	when corresponding `MediaFile` object is deleted.
	"""
	if instance.file_field:
		if os.path.isfile(instance.file_field.path):
			os.remove(instance.file_field.path)
