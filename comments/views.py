from django.shortcuts import render, redirect
from django.views import View, generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from posts.models import Post
from .models import Comment
from .forms import CommentForm

# Create your views here.

class CommentCreateView(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		form = CommentForm(request.POST)
		if form.is_valid:
			# post = Post.objects.get(pk=kwargs['post_pk'])
			form = form.save(commit=False)
			form.user = request.user 
			form.post = Post.objects.get(pk=kwargs['post_pk'])
			form.save()
		return redirect(reverse('post_detail', kwargs={'pk':kwargs['post_pk']}))

comment_create = CommentCreateView.as_view()

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
	model = Comment 
	fields = ['content',]
	template_name = 'comments/comment_update.html'

	def test_func(self):
		return self.request.user == self.get_object().user 

comment_update = CommentUpdateView.as_view()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
	model = Comment 
	template_name = 'comments/comment_delete.html'
	
	def get_success_url(self):
		return Comment.objects.get(pk=self.kwargs['pk']).post.get_absolute_url()

	def test_func(self):
		return self.request.user == self.get_object().user 

comment_delete = CommentDeleteView.as_view()
