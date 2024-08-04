from django.db.models import Q
from .forms import SearchForm
from django.utils import timezone
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from TimeCapsuleManagement.forms import CommentForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from TimeCapsuleManagement.models import Capsule, Subscription


def search(request):
    comment_form = CommentForm()
    # Handle the toggle subscription action within the search request
    if 'toggle_subscription' in request.GET and request.user.is_authenticated:
        capsule_id = request.GET.get('capsule_id')
        if capsule_id:
            capsule = get_object_or_404(Capsule, pk=capsule_id)
            user_profile = request.user  # Direct use since UserProfile is the user model
            # Toggle the subscription status
            subscription, created = Subscription.objects.get_or_create(
                user=user_profile,
                capsule=capsule,
            )
            if not created:
                # If the subscription exists, delete it (unsubscribe)
                subscription.delete()
            # Redirect to avoid processing the toggle action again if the page is refreshed
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # Continue with search functionality if not toggling a subscription
    form = SearchForm(request.GET)
    capsules = Capsule.objects.prefetch_related('media', 'comments', 'subscribers').filter(is_published=True)
    if form.is_valid():
        query = form.cleaned_data.get('q', '')
        if query:
            capsules = capsules.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(owner__username__icontains=query)
            )
    # Filtering logic
    status = request.GET.get('status')
    sealed = request.GET.get('sealed')
    date = request.GET.get('date')
    if status == 'public':
        capsules = capsules.filter(is_public=True)
    elif status == 'private':
        capsules = capsules.filter(is_public=False)
    if sealed == 'unsealed':
        capsules = capsules.filter(unsealing_date__lte=timezone.now())
    elif sealed == 'sealed':
        capsules = capsules.filter(unsealing_date__gt=timezone.now())
    if date:
        capsules = capsules.filter(unsealing_date__date=date)
    # Sorting logic
    sort = request.GET.get('sort')
    if sort == 'date':
        capsules = capsules.order_by('unsealing_date')
    elif sort == 'name':
        capsules = capsules.annotate(lower_name=Lower('name')).order_by('lower_name')
    # Check subscription status for each capsule for the current user (if logged in)
    if request.user.is_authenticated:
        user_profile = request.user  # Direct use since UserProfile is the user model
        for capsule in capsules:
            capsule.is_subscribed = Subscription.objects.filter(user=user_profile, capsule=capsule).exists()
            print(capsule.is_subscribed)
    context = {
        'form': form,
        'posts': capsules,
        'comment_form': comment_form
    }
    return render(request, 'search.html', context)


@login_required
def toggle_subscription(request, capsule_id):
    # Fetch the capsule object based on the provided capsule_id
    capsule = get_object_or_404(Capsule, pk=capsule_id)
    # Use request.user directly since it is an instance of UserProfile
    user_profile = request.user
    # Check if a subscription already exists for this user and capsule
    subscription, created = Subscription.objects.get_or_create(
        user=user_profile,
        capsule=capsule,
    )
    if not created:
        # If the subscription exists, delete it (unsubscribe)
        subscription.delete()
    # Redirect to the previous page or a specific page after toggling the subscription
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
