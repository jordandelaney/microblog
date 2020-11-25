from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

# Get custom user model
User = get_user_model()

def register(request):
    """Register a new user"""
    if request.user.is_authenticated:
        raise Http404
    if request.method != 'POST':
        #Display blank registration form
        form = CustomUserCreationForm()
    else:
        #Process completed form
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #Log the user in and then redirect to home page.
            login(request, new_user)
            return redirect('blog:index')

    #Display a blank or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)

@login_required
def profile(request):
    """Display a page with user profile info"""
    user = get_object_or_404(CustomUser, pk=request.user.pk)
    context = {
        'user': user
    }
    return render(request, 'accounts/profile.html', context)