from TimeCapsuleManagement.models import Subscription
from django.core.exceptions import ObjectDoesNotExist


def create_subscription(user_id, capsule_id, approved=False):
    """
    Create a new subscription.
    Args:
        user_id: The user who is subscribing.
        capsule_id: The ID of the capsule to subscribe to.
        approved: Whether the subscription is approved (default is False).
    Returns:
        The newly created Subscription object.
    """
    try:
        subscription = Subscription.objects.create(
            user=user_id,
            capsule_id=capsule_id,
            approved=approved
        )
        return subscription
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while creating a subscription: {e}")
        return None


def get_subscription_by_id(subscription_id):
    """
    Retrieve a specific subscription by its ID.
    Args:
        subscription_id: The ID of the subscription to retrieve.
    Returns:
        Subscription object if found, None otherwise.
    """
    try:
        return Subscription.objects.get(id=subscription_id)
    except ObjectDoesNotExist:
        return None
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while retrieving subscription {subscription_id}: {e}")
        return None

def get_subscriptions_for_capsule(capsule_id):
    """
    Retrieve all subscriptions associated with a specific capsule.
    Args:
        capsule_id: The ID of the capsule.
    Returns:
        QuerySet of Subscription objects related to the specified capsule.
    """
    try:
        return Subscription.objects.filter(capsule_id=capsule_id)
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while retrieving subscriptions for capsule {capsule_id}: {e}")
        return None


def get_subscriptions_for_user(user_id):
    """
    Retrieve all subscriptions associated with a specific user.
    Args:
        user_id: The user profile.
    Returns:
        QuerySet of Subscription objects related to the specified user.
    """
    try:
        return Subscription.objects.filter(user=user_id)
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while retrieving subscriptions for user {user_id}: {e}")
        return None


def update_subscription_by_id(subscription_id, approved):
    """
    Update an existing subscription.
    Args:
        subscription_id: The ID of the subscription to update.
        approved: Whether the subscription is approved.
    Returns:
        The updated Subscription object.
    """
    try:
        subscription = Subscription.objects.get(id=subscription_id)
        subscription.approved = approved
        subscription.save()
        return subscription
    except ObjectDoesNotExist:
        return None
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while updating subscription {subscription_id}: {e}")
        return None


def delete_subscription_by_id(subscription_id):
    """
    Delete a subscription.
    Args:
        subscription_id: The ID of the subscription to delete.
    """
    try:
        subscription = Subscription.objects.get(id=subscription_id)
        subscription.delete()
        return True
    except ObjectDoesNotExist:
        return None
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while deleting subscription {subscription_id}: {e}")
        return None
