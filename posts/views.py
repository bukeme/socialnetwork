from django.shortcuts import render
from django.views import generic 
from django.views import View 
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm

# Create your views here.

class HomePageView(LoginRequiredMixin, generic.TemplateView):
	template_name = 'posts/home_page.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['p_form'] = PostForm()
		return context

home_page = HomePageView.as_view()

class PostCreateView(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		form = PostForm(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.user = request.user 
			form.save()
			return redirect('home')

post_create = PostCreateView.as_view()
