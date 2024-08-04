import mimetypes
from datetime import datetime
from django.views import View
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from .forms import CapsuleForm, CommentForm
from AuthenticationSystem.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Capsule, CapsuleContent, Subscription
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect


# Create your views here.


class Index(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        # Logic to fetch posts, similar to your FBV
        posts = Capsule.objects.filter(subscribers__user=request.user).exclude(is_published=False).order_by('name')
        users = UserProfile.objects.all()
        comment_form = CommentForm()
        show_welcome = None
        message = None
        # Process each post
        for post in posts:
            print(post.owner.profilepic)
        # Welcome message and last visit handling
        if request.user.is_authenticated:
            welcome_cookie = f'show_welcome_message_{request.user}'
            cookie_name = f'last_visit_{request.user.username}'
            show_welcome = request.COOKIES.get(welcome_cookie, 'false') == 'true'
            last_visit = request.COOKIES.get(cookie_name)
            if show_welcome:
                if last_visit:
                    last_visit_time = datetime.strptime(last_visit, '%Y-%m-%d %H:%M:%S')
                    message = f"Welcome back {request.user.username}! Your last visit today was: {last_visit_time.strftime('%I:%M %p')}"
                else:
                    message = "Welcome to our site!"
        # Subscription checking
        if request.user.is_authenticated:
            user_profile = request.user
            for capsule in posts:
                capsule.is_subscribed = Subscription.objects.filter(user=user_profile, capsule=capsule).exists()
                print(capsule.is_subscribed)
        response = render(request, 'home.html', {
            'posts': posts,
            'users': users,
            'comment_form': comment_form,
            'message': message
        })
        # Cookie handling for welcome message and last visit
        if show_welcome:
            welcome_cookie = f'show_welcome_message_{request.user}'
            response.delete_cookie(welcome_cookie)
            now = timezone.now()
            end_of_day = timezone.datetime(now.year, now.month, now.day, 23, 59, 59,
                                           tzinfo=timezone.get_default_timezone())
            max_age = (end_of_day - now).total_seconds()
            last_visit_cookie_name = f'last_visit_{request.user}'
            time_now = now.astimezone(timezone.get_default_timezone())
            response.set_cookie(last_visit_cookie_name, time_now.strftime('%Y-%m-%d %H:%M:%S'), max_age=int(max_age))
        return response


@login_required
def my_capsules(request):
    comment_form = CommentForm()
    owner = UserProfile.objects.get(id=request.user.id)
    capsule_list = Capsule.objects.prefetch_related('media').prefetch_related('comments').filter(owner=owner)
    if request.method == 'POST':
        data = request.POST.copy()
        data['owner'] = request.user.id
        form = CapsuleForm(data, request.FILES)
        if form.is_valid():
            capsule = form.save()
            # Handle the uploaded files for CapsuleContent
            files = request.FILES.getlist('capsule_contents')
            for file in files:
                mime_type, _ = mimetypes.guess_type(file.name)
                file_type = 'photo'  # Default file type
                if mime_type:
                    if mime_type.startswith('image/'):
                        file_type = 'photo'
                    elif mime_type.startswith('video/'):
                        file_type = 'video'
                # Create a CapsuleContent object for each file
                CapsuleContent.objects.create(
                    file=file,
                    capsule=capsule,
                    file_type=file_type,  # Use the determined file type
                )
            messages.success(request, 'Time Capsule created successfully!')
            redirect_url = reverse('TimeCapsuleManagement:my_capsules')
            return HttpResponse(f'success|{redirect_url}')
        else:
            messages.error(request, 'An error occurred while creating the capsule, please try again.')
            redirect_url = reverse('TimeCapsuleManagement:my_capsules')
            return HttpResponse(f'error|{redirect_url}')
    else:
        form = CapsuleForm()
    return render(request, 'my_capsules.html',
                  {'form': form, 'capsule_list': capsule_list, 'comment_form': comment_form})


@login_required
def edit_capsule(request, capsule_id):
    capsule = get_object_or_404(Capsule, id=capsule_id, owner=request.user)
    if request.method == 'GET':
        data = {
            'name': capsule.name,
            'description': capsule.description,
            'unsealing_date': capsule.unsealing_date.strftime('%Y-%m-%dT%H:%M'),
            'is_public': capsule.is_public,
            'is_published': capsule.is_published,
        }
        return JsonResponse(data)
    elif request.method == 'POST':
        data = request.POST.copy()
        data['owner'] = request.user.id
        form = CapsuleForm(data, request.FILES, instance=capsule)
        if form.is_valid():
            updated_capsule = form.save()
            contents_to_delete = request.POST.getlist('filesToDelete', [])
            CapsuleContent.objects.filter(id__in=contents_to_delete).delete()
            files = request.FILES.getlist('capsule_contents')
            for file in files:
                mime_type, _ = mimetypes.guess_type(file.name)
                file_type = 'photo'  # Default file type
                if mime_type:
                    if mime_type.startswith('image/'):
                        file_type = 'photo'
                    elif mime_type.startswith('video/'):
                        file_type = 'video'
                CapsuleContent.objects.create(
                    file=file,
                    capsule=updated_capsule,
                    file_type=file_type
                )
            messages.success(request, 'Capsule updated successfully!')
            redirect_url = reverse('TimeCapsuleManagement:my_capsules')
            return HttpResponse(f'success|{redirect_url}')
        else:
            messages.error(request, 'An error occurred while updating the capsule.')
            redirect_url = reverse('TimeCapsuleManagement:my_capsules')
            return HttpResponse(f'error|{redirect_url}')


@login_required
def get_capsule_contents(request, capsule_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            contents = CapsuleContent.objects.filter(capsule_id=capsule_id).values('id', 'file', 'file_type')
            return JsonResponse(list(contents), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def delete_capsule(request, capsule_id):
    if request.method == "POST":
        capsule = get_object_or_404(Capsule, id=capsule_id)
        capsule.delete()
        messages.success(request, "Capsule deleted successfully!")
        return redirect('TimeCapsuleManagement:my_capsules')
    else:
        messages.error(request, "An error occurred, please try again.")
        return redirect('TimeCapsuleManagement:my_capsules')


@login_required
def post_comment(request, capsule_id):
    capsule = Capsule.objects.get(pk=capsule_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.capsule = capsule
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment saved successfully!")
            referer_url = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(referer_url)
    else:
        referer_url = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(referer_url)
