from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

from blog.models import BlogPost

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class Comment(models.Model):
	user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
	# post = models.ForeignKey(BlogPost, null=True, on_delete=models.SET_NULL)
	content_type = models.ForeignKey(ContentType, default=1, on_delete=models.CASCADE, null=True)
	object_id = models.PositiveIntegerField(default=1, null=True)
	content_object = GenericForeignKey('content_type', 'object_id')
	content	= models.TextField()
	timestamp = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.user.username)