from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentProfileForm
from .models import StudentProfile


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_setup(request):
    profile = StudentProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully.')
            return redirect('accounts:profile')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'accounts/profile_setup.html', {'form': form})


@login_required
def profile_edit(request):
    profile = StudentProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def profile_view(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})
