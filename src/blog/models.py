from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from comments.models import Comment

from django.contrib.contenttypes.models import ContentType

User = settings.AUTH_USER_MODEL

class BlogPostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now)

    def search(self, query):
        lookup = (
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(slug__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query) |
                    Q(user__username__icontains=query)
                    )

        return self.filter(lookup)

class BlogPostManager(models.Manager):
	def get_queryset(self):
		return BlogPostQuerySet(self.model, using=self._db)

	def published(self):
		return self.get_queryset().published()

	def search(self, query=None):
		if query is None:
			return self.get_queryset().none()
		return self.get_queryset().published().search(query)

# Create your models here.
class BlogPost(models.Model):
	# id = midels.IntegerField() # pk
	user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
	title = models.CharField(max_length=150)
	image = models.ImageField(upload_to='image/', blank=True, null=True)
	slug = models.SlugField(unique=True)
	content = models.TextField(null=True, blank=True)
	publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	objects = BlogPostManager()

	class Meta:
		ordering = ['-publish_date', '-updated', '-timestamp']
		verbose_name = "blogpost"

	def __str__(self):
		return self.title

	# Convention
	def get_absolute_url(self):
		return f"/blog/{self.slug}"

	def get_edit_url(self):
		return f"/blog/{self.slug}/edit"

	def get_delete_url(self):
		return f"{self.get_absolute_url}/delete"

	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type


	