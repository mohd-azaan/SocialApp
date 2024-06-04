from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required
from random import sample
from .models import Post
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
    

def explore(request):
    # Retrieve all posts
    all_posts = Post.objects.all()
    # Randomize the posts
    # randomized_posts = sample(list(all_posts), len(all_posts))
    return render(request, 'posts/explore.html', {'posts': all_posts})

@login_required
def like_post(request):
    print('here')
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    return redirect('explore')