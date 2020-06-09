from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

# from blog.models import BlogPost

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CommentManager(models.Manager):
	def filter_by_instance(self, obj):
		content_type = ContentType.objects.get_for_model(obj.__class__)
		obj_id = obj.id
		qs = super(CommentManager, self).filter(content_type = content_type, object_id=obj_id)
		return qs

class Comment(models.Model):
	user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
	# post = models.ForeignKey(BlogPost, null=True, on_delete=models.SET_NULL)
	content_type = models.ForeignKey(ContentType, default=1, on_delete=models.CASCADE, null=True)
	object_id = models.PositiveIntegerField(default=1, null=True)
	content_object = GenericForeignKey('content_type', 'object_id')
	content	= models.TextField()
	timestamp = models.DateTimeField(auto_now=True)
	objects=CommentManager()

	def __str__(self):
		return str(self.user.username)

