from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostCreateForm, CommentForm
from django.contrib.auth.decorators import login_required
from random import sample
from .models import Post
from users.models import Relationship
from django.views.decorators.cache import cache_control

# Create your views here.

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('index')
    else:
        form = PostCreateForm(data=request.GET)
    return render(request, 'posts/create_post.html', {
        'form': form,
    })
    

# @login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def explore(request):
    # Initialize the comment form and following_users to default values
    comment_form = CommentForm()
    following_users = Relationship.objects.none()

    # Check if the request method is POST
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        comment_form = CommentForm(data=request.POST)
        comment = request.POST.get('body')

        if not comment:
            return redirect('explore')
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            new_comment.post = post
            new_comment.posted_by = request.user
            new_comment.save()
            return redirect('explore')
    else:
        if request.user.is_authenticated:
            following_users = Relationship.objects.filter(follower=request.user).values_list('followed__id', flat=True)
    
    all_posts = Post.objects.all()
    return render(request, 'posts/explore.html', {'posts': all_posts, 'comment_form': comment_form, 'following_users': following_users})


@login_required
def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    return redirect('explore')




