from django.db import models


class SharedFile(models.Model):
	name = models.CharField(max_length=255, blank=True)
	file = models.FileField(upload_to="uploads/")
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return self.name or self.file.name
