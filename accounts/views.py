from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentProfileForm
from .models import StudentProfile
from academics.models import Subject


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
def subject_select(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    if request.method == 'POST':
        selected_ids = request.POST.getlist('subjects')
        valid_ids = set(
            Subject.objects.filter(pk__in=selected_ids).values_list('pk', flat=True)
        )
        profile.subjects.set(valid_ids)
        messages.success(request, 'Subject selection updated.')
        return redirect('accounts:profile')
    return render(request, 'accounts/subject_select.html', {
        'profile': profile,
        'subjects': Subject.objects.all(),
        'selected_ids': set(profile.subjects.values_list('pk', flat=True)),
    })


@login_required
def profile_view(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})
