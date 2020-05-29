from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
	# id = midels.IntegerField() # pk
	title = models.TextField()
	slug = models.SlugField(unique=True)
	content = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.title