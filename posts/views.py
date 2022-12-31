from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic 
from django.views import View 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from comments.forms import CommentForm
from comments.models import Comment 
from .forms import PostForm
from .models import Post
from .mixins import AjaxRequiredOnly

# Create your views here.

class HomePageView(LoginRequiredMixin, generic.TemplateView):
	template_name = 'posts/home_page.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['posts'] = Post.objects.all()
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

class PostDetailView(LoginRequiredMixin, generic.DetailView):
	model = Post 

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['c_form'] = CommentForm()
		context['comments'] = self.get_object().comment_set.all()
		return context 

post_detail = PostDetailView.as_view()

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
	model = Post 
	fields = ['content',]
	template_name = 'posts/post_update.html'

	def test_func(self):
		return self.request.user == self.get_object().user 

post_update = PostUpdateView.as_view()

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
	model = Post 
	template_name = 'posts/post_delete.html'
	success_url = reverse_lazy('home')

	def test_func(self):
		return self.request.user == self.get_object().user 

post_delete = PostDeleteView.as_view()

class PostLikeView(AjaxRequiredOnly, View):
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return JsonResponse({'status': 'not logged in'})
		post = Post.objects.get(pk=kwargs['pk'])
		next_action = None

		if request.user in post.likes.all():
			post.likes.remove(request.user)
			action = 'Like'
		else:
			post.likes.add(request.user)
			action = 'Liked'
		return JsonResponse({'status': 'ok', 'action': action})

post_like = PostLikeView.as_view()

# def post_like(request, pk):
# 	if not request.user.is_authenticated:
# 		return JsonResponse({'status': 'not logged in'})
# 	post = Post.objects.get(pk=pk)
# 	next_action = None

# 	if request.user in post.likes.all():
# 		post.likes.remove(request.user)
# 		action = 'Like'
# 	else:
# 		post.likes.add(request.user)
# 		action = 'Liked'
# 	return JsonResponse({'status': 'ok', 'action': action})


