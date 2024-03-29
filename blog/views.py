from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

class PostListView(ListView):
    model = Post
    template_name= 'blog/home.html' #<app>/<model>_<viewport>.html
    context_object_name = 'posts' # whatever is the name you gave to template
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name= 'blog/user_posts.html' #<app>/<model>_<viewport>.html
    context_object_name = 'posts' # whatever is the name you gave to template
    paginate_by = 5
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form: BaseModelForm):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form: BaseModelForm):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Home'
    }
    #return HttpResponse('<h1>Blog Home</h1>')
    return render(request, 'blog/home.html',context)

def about(request):
    return render(request, 'blog/about.html',{'title': 'About'})
