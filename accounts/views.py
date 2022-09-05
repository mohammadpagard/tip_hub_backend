# Django packages
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.utils.crypto import get_random_string
# Third party apps
import ghasedakpack
import random
from uuid import uuid4
# Local apps
from .models import User, OtpCode
from . import forms


SMS = ghasedakpack.Ghasedak("API KEY")


class UserLoginView(View):
    form_class = forms.UserLoginForm
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


class UserRegisterView(View):
    form_class = forms.UserRegisterForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class

        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            cd = form.cleaned_data
            SMS.verification({
                'receptor': cd['phone_number'],
                'type': 1,
                'template': 'TEMPLATE NAME',
                'param1': random_code
            })
            token = str(uuid4())
            OtpCode.objects.create(phone=cd['phone_number'], code=random_code, token=token)
            print(random_code)
            return redirect(reverse('accounts:check_otp') + f"?token={token}")

        context = {'form': form}
        return render(request, self.template_name, context)


class CheckOtpView(View):
    form_class = forms.CheckOtpForm
    template_name = 'accounts/check_otp.html'

    def get(self, request):
        form = self.form_class

        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        token = request.GET.get('token')
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if OtpCode.objects.filter(code=cd['code'], token=token).exists():
                otp = OtpCode.objects.get(token=token)
                user, is_created = User.objects.get_or_create(phone_number=otp.phone)
                login(request, user)
                otp.delete()
                return redirect('home:home')

        context = {'form': form}
        return render(request, self.template_name, context)


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
    form_class = forms.UserEditProfileForm
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
