from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Profile, Relationship
from posts.models import Post
from posts import models as postsmodel
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.decorators.cache import cache_control
from posts.forms import CommentForm
# Create your views here.

def chat(request, logged_user_id, to_chat_user_id):
    username = User.objects.get(pk=to_chat_user_id)
    return render(request, "users/chat.html", {
        'username': username,
    })

def chat_room(request):
    # Your logic to fetch messages and other details of the chat
    return render(request, 'users/chat_list.html')

@login_required
def index(request):
    profile = Profile.objects.filter(user=request.user).first()
    posts = postsmodel.Post.objects.filter(user=request.user)
    num_posts = len(posts)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        comment_form = CommentForm(data=request.POST)
        comment = request.POST.get('body')

        if not comment:
            return redirect('index')
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            new_comment.post = post
            new_comment.posted_by = request.user
            new_comment.save()
            return redirect('index')
    # Fetching following users
    following_users = Relationship.objects.filter(follower=request.user)

    # Fetching followers users
    followers_users = Relationship.objects.filter(followed=request.user)
    return render(
        request,
        "users/index.html",
        {
            "posts": posts,
            "profile": profile,
            "num_posts": num_posts,
            "following_users": following_users,
            "followers_users": followers_users,
        },
    )


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )
            if user:
                login(request, user)
                return redirect("index")
    form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect("login")

    user_form = UserRegistrationForm()
    return render(request, "users/register.html", {"user_form": user_form})


@login_required
def editUser(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("index")

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "users/userEdit.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )



@login_required
def follow(request, user_id):
    followed_user = User.objects.get(pk=user_id)
    Relationship.objects.create(follower=request.user, followed=followed_user)
    follower_count = followed_user.followers_set.count()
    return JsonResponse({"followed": True, "follower_count": follower_count})


@login_required
def unfollow(request, user_id):
    followed_user = User.objects.get(pk=user_id)
    Relationship.objects.filter(follower=request.user, followed=followed_user).delete()
    follower_count = followed_user.followers_set.count()
    return JsonResponse({"followed": False, "follower_count": follower_count})


from django.http import JsonResponse
from .models import Relationship



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_profile(request, user_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        comment_form = CommentForm(data=request.POST)
        comment = request.POST.get('body')

        if not comment:
            return redirect('user_profile', user_id=user_id)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            new_comment.post = post
            new_comment.posted_by = request.user
            new_comment.save()
            return redirect('user_profile', user_id=user_id)
        
    profile = Profile.objects.filter(user=user_id).first()
    posts = postsmodel.Post.objects.filter(user=user_id)
    num_posts = len(posts)
    user_ = User.objects.get(pk=user_id)
    following_users = Relationship.objects.filter(follower=user_id)
    # Fetching followers users
    followers_users = Relationship.objects.filter(followed=user_id)
    followers_user_ids = Relationship.objects.filter(followed=user_id).values_list('follower_id', flat=True)    # print('here')
    return render(
        request,
        "users/user_profile.html",
        {
            "posts": posts,
            "profile": profile,
            "num_posts": num_posts,
            "following_users": following_users,
            "followers_users": followers_users,
            "user_": user_,
            "followers_user_ids":followers_user_ids,
        },
    )


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def follow_unfollow(request):
    if request.method == "POST" and request.user.is_authenticated:
        print("here in the follow unfollow")
        user_id = request.POST.get("user_id")
        user_to_follow = User.objects.get(pk=user_id)
        relationship = Relationship.objects.filter(
            follower=request.user, followed=user_to_follow
        )
        # post = get_object_or_404(User, id=post_id)
        if relationship.exists():
            print("method")
            relationship.delete()
        else:
            Relationship.objects.create(follower=request.user, followed=user_to_follow)
        return redirect("explore")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search_users(request):
    query = request.GET.get("q", "")

    # Perform the search
    if query:
        users = User.objects.filter(Q(username__icontains=query))
    else:
        users = User.objects.all()

    # Fetching the relationships for the current logged-in user
    if request.user.is_authenticated:
        following_users = Relationship.objects.filter(
            follower=request.user
        ).values_list("followed__id", flat=True)
        followers_users = Relationship.objects.filter(
            followed=request.user
        ).values_list("follower__id", flat=True)
    else:
        following_users = []
        followers_users = []

    return render(
        request,
        "users/search.html",
        {
            "following_users": following_users,
            "followers_users": followers_users,
            "users": users,
            "query": query,
        },
    )
