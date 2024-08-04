import os
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from TimeCapsuleManagement.models import Capsule
from django.contrib.auth import views as auth_views
from TimeCapsuleManagement.forms import CommentForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from AuthenticationSystem.models import UserProfile, UserVisit
from AuthenticationSystem.crud_operations.auth_operations import create_user
from .forms import CustomLoginForm, CustomSignupForm, EditProfileForm, CustomPasswordResetForm
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


def verify_email(request, verification_token):
    try:
        user = UserProfile.objects.get(email_verification_token=verification_token)
        user.email_verified = True
        user.save()
        messages.success(request, 'Your email has been successfully verified.')
        return redirect('AuthenticationSystem:user_login')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Invalid verification token.')
        return redirect('AuthenticationSystem:user_login')


def send_verification_email(user):
    verification_token = get_random_string(length=32)
    user.email_verification_token = verification_token
    user.save()
    verification_url = '/verify_email/{}/'.format(verification_token)
    subject = 'Verify your email address'
    message = f'Click the following link to verify your email address: http://localhost:8000{verification_url}'
    recipient_list = [user.email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    return verification_url


def check_username_availability(request):
    if request.method == 'GET' and 'username' in request.GET:
        username = request.GET['username']
        if UserProfile.objects.filter(username__iexact=username).exists():
            return JsonResponse({'available': False})
        else:
            return JsonResponse({'available': True})
    return JsonResponse({'error': 'Invalid request'})


def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.email_verified:
                login(request, user)
                response = redirect('TimeCapsuleManagement:home')

                # Calculate max_age for the cookie to expire at the end of the day
                now = timezone.now()
                end_of_day = timezone.datetime(now.year, now.month, now.day, 23, 59, 59,
                                               tzinfo=timezone.get_default_timezone())
                max_age = (end_of_day - now).total_seconds()

                new_visit_cookie_name = f'show_welcome_message_{user.username}'
                response.set_cookie(new_visit_cookie_name, 'true',
                                    max_age=int(max_age))  # Expires at the end of the day
                return response
            else:
                if user is None:
                    messages.error(request, 'Invalid username or password')
                elif not user.email_verified:
                    messages.error(request, 'Email is not verified. Please verify your email.')
                return redirect('AuthenticationSystem:user_login')
    else:
        form = CustomLoginForm()
    return render(request, 'user_login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('SearchCapsule:capsule_search')


def user_signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            if UserProfile.objects.filter(username__iexact=username).exists():
                messages.error(request, 'A user with that username already exists.')
                return redirect('AuthenticationSystem:user_signup')

            if UserProfile.objects.filter(email__iexact=email).exists():
                messages.error(request, 'A user with that email already exists.')
                return redirect('AuthenticationSystem:user_signup')

            # Create user but mark email as not verified
            user = create_user(username, password, email)
            user.email_verified = False
            user.save()

            # Send verification email
            verification_url = send_verification_email(user)

            messages.success(request, 'User created successfully. Please verify your email.')

            return redirect('AuthenticationSystem:user_login')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, f"{error}")
    else:
        form = CustomSignupForm()
    return render(request, 'user_signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        owner = UserProfile.objects.get(id=request.user.id)
        if 'profile_submit' in request.POST:  # Check if profile form is submitted
            profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                username = profile_form.cleaned_data['username']
                first_name = profile_form.cleaned_data['first_name']
                last_name = profile_form.cleaned_data['last_name']
                bio = profile_form.cleaned_data['bio']
                print(profile_form.cleaned_data['username'])
                if not UserProfile.objects.filter(username=profile_form.cleaned_data['username']).exists():
                    profile_form.save()
                    messages.success(request, f'{owner} profile updated')
                    response = redirect('AuthenticationSystem:profile')
                    response.set_cookie('numvisit', owner.numofvisits)
                    return response

                else:
                    profile_form.instance.username = owner.username
                    profile_form.instance.bio = bio
                    profile_form.instance.first_name = first_name
                    profile_form.instance.last_name = last_name
                    profile_form.save()

                    messages.success(request, "Profile updated but the specified username is already taken")
                    response = redirect('AuthenticationSystem:profile')
                    response.set_cookie('numvisit', owner.numofvisits)
                    return response


        elif 'password_submit' in request.POST:  # Check if password form is submitted
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important for keeping the user logged in
                messages.success(request, 'Your password was successfully updated!')
                return redirect('AuthenticationSystem:profile')
            else:
                print(password_form.errors)
                messages.success(request, f'Meet the requirements for password change {password_form.errors}')
                return redirect('AuthenticationSystem:profile')

    else:

        owner = UserProfile.objects.get(id=request.user.id)
        # posts = Capsule.objects.prefetch_related('media').prefetch_related('comments').filter(owner=owner)
        # users = UserProfile.objects.all()
        # comment_form = CommentForm()
        password_form = PasswordChangeForm(request.user)
        form = EditProfileForm(instance=request.user)
        # user_history_session = request.session.get('user_history', [])
        user_history_database = UserVisit.objects.filter(user=request.user).order_by('-timestamp')
        response = render(request, 'profile.html', {
                                                'cur_user': owner,
                                                'form': form, 'password_form': password_form,
                                                'user_history': user_history_database[:7], 'nv': owner.numofvisits})
        response.set_cookie('numvisit', owner.numofvisits)
        # update_user_history(request)
        return response


@login_required
def update_user_history(request):
    if request.method == "POST" and request.user.is_authenticated:
        # Store visit history in the session
        user_history = request.session.get('user_history', [])
        user_history.append({'page': request.path, 'timestamp': timezone.now().isoformat()})
        request.session['user_history'] = user_history
        user_profile = UserProfile.objects.get(id=request.user.id)
        user_profile.numofvisits = user_profile.numofvisits + 1
        user_profile.save()
        UserVisit.objects.create(user=request.user, page=request.path)


@login_required
def update_profile_picture(request):
    if request.method == "POST" and request.FILES.get('profilepic'):
        user_profile = request.user
        old_profilepic_path = user_profile.profilepic.path if user_profile.profilepic else None
        user_profile.profilepic = request.FILES['profilepic']
        user_profile.save()
        if old_profilepic_path and os.path.exists(old_profilepic_path):
            os.remove(old_profilepic_path)
    return render(request, 'profile.html')


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = '/accounts/password_reset/done/'
    form_class = CustomPasswordResetForm


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('AuthenticationSystem:password_reset_complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
