from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from .forms import ContactForm

def home_page(request):
	my_title = "Hello there..."
	if request.user.is_authenticated:
		context = {'title':my_title, 'my_list': [1, 2, 3, 4, 5]}
	return render(request, "home.html", context)

def about_page(request):
	return render(request, "about.html", {'title':"About us"})

def contact_page(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data)
	context = {
	 	"title":"Contact us",
	 	"form":form
	 	}
	return render(request, "form.html", context)

def example_page(request):
	context 	  = {'title':"Example"}
	template_name = "about.html"
	template_obj = get_template(template_name)
	return HttpResponse(template_obj.render(context))