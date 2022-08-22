# Django packages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
# Local apps
from .models import User
from .forms import UserRegisterForm, UserLoginForm, UserEditProfileForm


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        if request.user.is_authenticated:
            return redirect('home:home')

        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(
                phone_number=cd['phone_number'],
                email=cd['email'],
                fullname=cd['fullname'],
                password=cd['password1']
            )
            return redirect('home:home')

        context = {'form': form}
        return render(request, self.template_name, context)


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        if request.user.is_authenticated:
            return redirect('home:home')

        context = {'form': form}
        return render(request, 'accounts/login.html', context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, phone_number=cd['phone_number'], password=cd['password']
            )
            if user is not None:
                login(request, user)
                messages.success(request, "You're login is successfully", 'success')
                return redirect('home:home')
            messages.error(request, "You're username or password is wrong", 'danger')

        context = {'form': form}
        return render(request, self.template_name, context)


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home:home')


# User profile
class UserProfileView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        videos = user.videos.all()

        context = {
            'user': user,
            'videos': videos
        }
        return render(request, 'accounts/user_profile.html', context)


class UserEditProfileView(View):
    form_class = UserEditProfileForm
    template_name = 'accounts/edit_user_profile.html'

    def get(self, request):
        form = self.form_class(
            initial={
                'phone_number': request.user.phone_number,
                'email': request.user.email,
                'fullname': request.user.fullname,
                'age': request.user.age,
                'bio': request.user.bio,
                'image': request.user.image
            }
        )
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(
            data=request.POST,
            files=request.FILES,
            initial={
                'phone_number': request.user.phone_number,
                'email': request.user.email,
                'fullname': request.user.fullname,
                'age': request.user.age,
                'bio': request.user.bio,
                'image': request.user.image
            }
        )
        if form.is_valid():
            cd = form.cleaned_data
            request.user.phone_number = cd['phone_number']
            request.user.email = cd['email']
            request.user.fullname = cd['fullname']
            request.user.age = cd['age']
            request.user.bio = cd['bio']
            request.user.image = cd['image']
            request.user.save()
        return redirect('accounts:profile', request.user.id)


# User reset password
class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
