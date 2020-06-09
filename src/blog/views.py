from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType

# from django.utils import timezone
from comments.models import Comment
from .models import BlogPost
from .forms import BlogPostForm, BlogPostModelForm
from comments.forms import CommentForm

# def blog_post_detail_page(request, slug):
# 	print("Django says", request.method, request.path, request.user)
# 	# queryset = BlogPost.objects.filter(slug=slug)
# 	# if queryset.count() == 0:
# 	# 	raise Http404
# 	# obj = queryset.first()
# 	# obj = BlogPost.objects.get(id=post_id)
# 	obj = get_object_or_404(BlogPost, slug=slug)
# 	template_name = "blog_post_detail.html"
# 	context = {"objects": obj}
# 	return render(request, template_name, context)

# CRUD

def blog_post_list_view(request):
	# list out objects
	# cloud be search
	# now = timezone.now()
	qs = BlogPost.objects.published() # queryset -> list of python objects
	if request.user.is_authenticated:
		my_qs = BlogPost.objects.filter(user=request.user)
		qs = (qs | my_qs).distinct()
	# qs = BlogPost.objects.filter(publish_date__lte=now)
	# qs = BlogPost.objects.filter(title__icontains='vs') # Filtrare pentru titluri care contin "vs"
	template_name = "blog/list.html"
	context = {'object_list': qs }
	return render(request, template_name, context)

# @login_required(login_url='/login')
@staff_member_required
def blog_post_create_view(request):
	# create objects
	# ? use a form
	form = BlogPostModelForm(request.POST or None, request.FILES or None)
	# Not authenticated user

	# if not request.user.is_authenticated:
	# 	return render(request, template_name, context)

	if form.is_valid():
		# Manipulation Data
		obj = form.save(commit=False)
		obj.user = request.user
		# obj.title = form.cleaned_data.get("title") + "0"
		obj.save()

		# form.save()
		form = BlogPostModelForm()
	template_name = "form.html"
	# template_name = "blog/create.html"
	context = {'form': form}
	return render(request, template_name, context)

def blog_post_detail_view(request, slug):
	# 1 object -> detail view
	obj = get_object_or_404(BlogPost, slug = slug)
	template_name = "blog/detail.html"
	# content_type = ContentType.objects.get_for_model(BlogPost)
	# obj_id = obj.id
	# comments = Comment.objects.filter(content_type = content_type, object_id=obj_id)

	# comments = Comment.objects.filter_by_instance(obj)
	comments = obj.comments
	initial_data = {"content_type":obj.get_content_type, "object_id":obj.id}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
		new_comment, created = Comment.objects.get_or_create(user= request.user, content_type= content_type, object_id = obj_id, content = content_data)

		if created:
			print("yeah it worked")

	context = {'object': obj, "comments":comments, 'comment_form':form}
	return render(request, template_name, context)

@staff_member_required
def blog_post_update_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	form = BlogPostModelForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
	
	# Nu este valid
	template_name = "form.html"
	context = {"title": f"Update {obj.title}", "form":form}
	return render(request, template_name, context)

@staff_member_required
def blog_post_delete_view(request, slug):
	obj = get_object_or_404(BlogPost, slug = slug)
	template_name = "blog/delete.html"
	if request.method == "POST":
		obj.delete()
		return redirect("/blog")
	context = {'object': obj}
	return render(request, template_name, context)

# def blog_post_create_view(request):
# 	# create objects
# 	# ? use a form
# 	form = BlogPostForm(request.POST or None)
# 	if form.is_valid():
# 		obj = BlogPost.objects.create(**form.cleaned_data)
# 		form = BlogPostForm()
# 	template_name = "form.html"
# 	# template_name = "blog/create.html"
# 	context = {'form': form}
# 	return render(request, template_name, context)

# obj = BlogPost.objects.create(title=title)

# obj = BlogPost()
# obj.title = title
# obj.save()


