from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from .forms import UserSignUpForm
from .models import User


# Create your views here.


@login_required
def profile(request):
    user = request.user
    if user.is_superuser:
        is_admin = True
    else:
        is_admin = False
    return render(request, 'accounts/profile.html', {'user': user, 'is_admin': is_admin})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_profile(request, id):
    User.objects.filter(id=id).delete()
    messages.success(request, 'Usuario eliminado exitosamente')
    return redirect('user_list')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'bio', 'website']
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user


def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = UserSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Usuario o contraseña incorrecta.')
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.bio = request.POST['bio']
        user.website = request.POST['website']
        user.save()
        messages.success(request, 'Perfil actualizado exitosamente!')
        return redirect('accounts:profile')
    else:
        return render(request, 'accounts/edit_profile.html', {'user': user})


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'accounts/about.html')
