from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Profile
from posts import models as postsmodel

# Create your views here.

@login_required
def index(request):
    profile = Profile.objects.filter(user=request.user).first()
    posts = postsmodel.Post.objects.filter(user=request.user)
    num_posts = len(posts)
    return render(request, 'users/index.html', {'posts': posts, 'profile':profile, "num_posts":num_posts})




def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect('index')
    form = LoginForm()
    return render(request, 'users/login.html', {"form": form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'users/registerDone.html')
    
    user_form = UserRegistrationForm()
    return render(request, 'users/register.html', {'user_form': user_form})

@login_required
def editUser(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('index')
            
    else :
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'users/userEdit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
    