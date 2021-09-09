from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, TemplateView, UpdateView
import uuid

from blog.forms import CommentForm
from blog.models import Blog, Comment, Like, Unlike


def blog(request):
    return redirect('home')


class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'blog/my_blog.html'


class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog/create.html'
    fields = ['title', 'content', 'cover']

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.title
        blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
        blog_obj.save()
        return redirect('home')


class UpdateBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'content', 'cover']
    template_name = 'blog/update.html'

    def get_success_url(self, **kwargs):
        if self.user== self.request.user:
            return reverse_lazy('detail', kwargs={'slug': self.object.slug})


class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'index.html'


@login_required(login_url='/accounts/login/')
def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    already_liked = Like.objects.filter(blog=blog, user=request.user)
    if already_liked:
        liked = True
    else:
        liked = False
    already_unliked = Unlike.objects.filter(blog=blog, user=request.user)
    if already_unliked:
        unliked = True
    else:
        unliked = False
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('detail', kwargs={'slug': slug}))
    context = {
        'blog': blog,
        'form': comment_form,
        'liked': liked,
        'unliked': unliked,
    }
    return render(request, 'blog/details.html', context)


@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)
    slug = blog.slug
    user = request.user
    already_liked = Like.objects.filter(blog=blog, user=user)
    already_unliked = Unlike.objects.filter(blog=blog, user=user)
    if already_unliked:
        already_unliked.delete()
    if not already_liked:
        liked_post = Like(blog=blog, user=user)
        liked_post.save()
        return HttpResponseRedirect(reverse('blog_detail', kwargs={'slug': slug}))
    context = {
        'blog': blog
    }
    return render(request, 'blog/details.html', context)


@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk=pk)
    slug = blog.slug
    user = request.user
    already_unliked = Unlike.objects.filter(blog=blog, user=user)
    already_liked = Like.objects.filter(blog=blog, user=user)
    if already_liked:
        already_liked.delete()
    if not already_unliked:
        unliked_post = Unlike(blog=blog, user=user)
        unliked_post.save()
        return HttpResponseRedirect(reverse('blog_detail', kwargs={'slug': slug}))
    context = {
        'blog': blog
    }
    return render(request, 'blog/details.html', context)
