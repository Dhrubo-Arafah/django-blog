from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect

from accounts.forms import UserProfileUpdate, ProfilePic
from accounts.models import UserProfile


def signup_form(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            form.save()
            user = authenticate(username=username, password=password)
            UserProfile.objects.create(user=user)
            if user is not None:
                login(request, user)
                return redirect('profile')
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


def login_form(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


@login_required(login_url='/accounts/login/')
def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/accounts/login/')
def profile(request):
    context = {}
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='/accounts/login/')
def user_update(request):
    current_user = request.user
    form = UserProfileUpdate(instance=current_user)
    if request.method == 'POST':
        form = UserProfileUpdate(data=request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {
        'form': form
    }
    return render(request, 'accounts/user_update.html', context)


@login_required(login_url='/accounts/login/')
def password_change(request):
    current_user = request.user
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(instance=current_user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('update_profile')
    context = {
        'form': form
    }
    return render(request, 'accounts/password_change.html', context)


@login_required(login_url='/accounts/login/')
def update_pro_pic(request):
    form = ProfilePic(instance=request.user.user_profile)
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {
        'form': form
    }
    return render(request, 'accounts/profile_pic.html', context)
