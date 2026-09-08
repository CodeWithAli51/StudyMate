from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


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


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
