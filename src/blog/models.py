from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class BlogPostQuerySet(models.QuerySet):
	def published(self):
		now = timezone.now()
		return self.filter(publish_date__lte=now)

class BlogPostManager(models.Manager):
	def get_queryset(self):
		return BlogPostQuerySet(self.model, using=self._db)

	def published(self):
		return self.get_queryset().published()

# Create your models here.
class BlogPost(models.Model):
	# id = midels.IntegerField() # pk
	user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
	title = models.CharField(max_length=150)
	image = models.FileField(upload_to='image/', blank=True, null=True)
	slug = models.SlugField(unique=True)
	content = models.TextField(null=True, blank=True)
	publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	objects = BlogPostManager()

	class Meta:
		ordering = ['-publish_date', '-updated', '-timestamp']

	def __str__(self):
		return self.title

	# Convention
	def get_absolute_url(self):
		return f"/blog/{self.slug}"

	def get_edit_url(self):
		return f"/blog/{self.slug}/edit"

	def get_delete_url(self):
		return f"{self.get_absolute_url}/delete"