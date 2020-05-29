from django.http import Http404
from django.shortcuts import render, get_object_or_404

from  .models import BlogPost

def blog_post_detail_page(request, slug):
	print("Django says", request.method, request.path, request.user)
	# queryset = BlogPost.objects.filter(slug=slug)
	# if queryset.count() == 0:
	# 	raise Http404
	# obj = queryset.first()
	# obj = BlogPost.objects.get(id=post_id)
	obj = get_object_or_404(BlogPost, slug=slug)
	template_name = "blog_post_detail.html"
	context = {"objects": obj}
	return render(request, template_name, context)

# CRUD

def blog_post_list_view(request):
	# list out objects
	# cloud be search
	qs = BlogPost.objects.all() # queryset -> list of python objects
	# qs = BlogPost.objects.filter(title__icontains='vs') # Filtrare pentru titluri care contin "vs"
	template_name = "blog/list.html"
	context = {'object_list': qs }
	return render(request, template_name, context)

def blog_post_create_view(request):
	# create objects
	# ? use a form
	template_name = "blog/create.html"
	context = {'form': None}
	return render(request, template_name, context)

def blog_post_detail_view(request, slug):
	# 1 object -> detail view
	obj = get_object_or_404(BlogPost, slug = slug)
	template_name = "blog/detail.html"
	context = {'object': obj}
	return render(request, template_name, context)

def blog_post_update_view(request):
	obj = get_object_or_404(BlogPost, slug = slug)
	template_name = "blog/update.html"
	context = {'object': obj, 'form':nOne}
	return render(request, template_name, context)

def blog_post_delete_view(request):
	obj = get_object_or_404(BlogPost, slug = slug)
	template_name = "blog/delete.html"
	context = {'object': obj}
	return render(request, template_name, context)







