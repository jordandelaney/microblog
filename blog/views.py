from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import random

from blog.models import BlogPost, Comment
from .forms import PostForm, CommentForm

# Get custom user model
User = get_user_model()

def check_post_owner(post, request):
    """Ensure request user owns the post"""
    if post.blogger != request.user:
        raise Http404

# Create your views here.
def index(request):
    posts = BlogPost.objects.filter(private=False)
    random_post = random.choice(posts)
    context = {
        'post': random_post
    }
    return render(request, 'blog/index.html', context=context)

class BlogPostListView(generic.ListView):
    """Generic list view for blog posts"""
    model = BlogPost
    paginate_by = 5

    def get_queryset(self):
        return BlogPost.objects.filter(private=False).order_by('-date_added')

class UserListView(generic.ListView):
    """General list view for all bloggers"""
    model = User
    paginate_by = 25

    def get_queryset(self):
        return User.objects.order_by('last_name')

def post_detail(request, pk, title):
    """Retrieves details for a specific post."""
    post = get_object_or_404(BlogPost, pk=pk)
    form = CommentForm()
    comments = post.comment_set.order_by('-date_added')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 5)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    # Check if post is private, if it is, and the request user != the owner of the post, redirect to 404. Otherwise render template.
    if post.private and request.user != post.blogger:
        raise Http404
    else:
        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'blog/post_detail.html', context=context)

# Retrieves blogger detail page, note that username is used in the url config rather than pk/id
def blogger_detail(request, username):
    """Retrieves details for a blogger detail page"""
    blogger = get_object_or_404(User, username=username)
    posts = BlogPost.objects.filter(blogger=blogger.pk).order_by('-date_added')[:5]
    context = {
        'blogger': blogger,
        'posts': posts,
    }
    return render(request, 'blog/blogger_detail.html', context=context)

# New Post
@login_required
def new_post(request):
    """Add a new blog post"""
    if request.method != 'POST':
        # No data submitted, create blank form
        form = PostForm()
    else: 
        # POST data submitted, process form
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blogger = request.user
            new_post.save()
            return redirect('blog:post-detail', new_post.pk, new_post.slug)

    # Display blank or invalid form
    context = {'form': form}
    return render(request, 'blog/new_post.html', context)

@login_required
def new_comment(request, pk):
    """Add a new comment to a BlogPost"""
    post = BlogPost.objects.get(pk=pk)
    if request.method == 'POST':
        # Data submitted, process form
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.owner = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('blog:post-detail', post.pk, post.slug)
    else:
        return Http404

@login_required
def edit_post(request, pk):
    """Edit an existing entry"""
    post = get_object_or_404(BlogPost, pk=pk)
    check_post_owner(post, request)

    if request.method != 'POST':
        #Intial request, pre-fill form with current post.
        form = PostForm(instance=post)
    else:
        # POST data submitted, process data:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:post-detail', post.pk, post.slug)

    context = {'form': form}
    return render(request, 'blog/edit_post.html', context)

# Delete a post
class BlogPostDelete(LoginRequiredMixin, DeleteView):
    login_url = 'accounts:login'
    model = BlogPost
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/delete_post.html'