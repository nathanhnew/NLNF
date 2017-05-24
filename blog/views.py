# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.forms import PostForm, CommentForm
from django.views.generic import (TemplateView, ListView,
								DetailView, CreateView, UpdateView,
								DeleteView)
from blog.models import Post, Comment

# Create your views here.
class IndexView(TemplateView):
	template_name = 'index.html'
	
class AboutView(TemplateView):
	template_name = 'about.html'

class PostListView(ListView):
	model = Post

	def get_queryset(self):
		return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
	model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
	login_url = '/login/'
	redirect_field_name = 'blog/post_list.html'
	form_class = PostForm
	model = Post

	def get_context_data(self,**kwargs):
		c = super(CreatePostView, self).get_context_data(**kwargs)
		user = self.request.user
		return c

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.title = form.instance.title.title()
		form.save()
		return super(CreatePostView, self).form_valid(form)

class PostUpdateView(LoginRequiredMixin,UpdateView):
	login_url = '/login/'
	redirect_field_name = 'blog/post_detail.html'
	form_class = PostForm
	model = Post

	# def get_object(self):
	# 	return get_object_or_404(Post, pk=self.request.GET.get('id'))

class PostDeleteView(LoginRequiredMixin,DeleteView):
	model=Post
	success_url = reverse_lazy('post_list')
	
class DraftListView(LoginRequiredMixin,ListView):
	login_url = '/login/'
	redirect_field_name = 'blog/post_list.html'
	model = Post
	template_name = 'blog/post_draft_list.html'

	def get_queryset(self):
		return Post.objects.filter(published_date__isnull=True).order_by('-create_date')

###################################################
###################################################
###												###
###			COMMENTS VIEW FUNCTIONS				###
###												###
###################################################
###################################################

@login_required
def post_publish(request,pk):
	post = get_object_or_404(Post,pk=pk)
	post.publish()
	return redirect('post_detail',pk=pk)

def add_comment_to_post(request,pk):
	post = get_object_or_404(Post,pk=pk)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('post_detail',pk=post.pk)
	else:
		form = CommentForm()
	return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
	comment = get_object_or_404(Comment,pk=pk)
	comment.approve()
	return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
	comment = get_object_or_404(Comment,pk=pk)
	post_pk = comment.post.pk
	comment.delete()
	return redirect('post_detail',pk=post_pk)