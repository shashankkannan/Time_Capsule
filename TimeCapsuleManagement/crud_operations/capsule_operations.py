from TimeCapsuleManagement.models import Capsule
from django.core.exceptions import ObjectDoesNotExist


def create_capsule(owner_id, name, description, is_public, unsealing_date):
    """
    Create a new capsule.
    Args:
        owner_id: The ID of the UserProfile who owns the capsule.
        name: The name of the capsule.
        description: A description of the capsule.
        is_public: Boolean indicating if the capsule is public.
        unsealing_date: The date and time when the capsule will be unsealed.
    Returns:
        The newly created Capsule object or None in case of an error.
    """
    try:
        capsule = Capsule.objects.create(
            owner=owner_id,
            name=name,
            description=description,
            is_public=is_public,
            unsealing_date=unsealing_date
        )
        return capsule
    except Exception as e:
        print(f"An error occurred while creating the capsule: {e}")
        return None


def get_capsule_by_id(capsule_id):
    """
    Retrieve a specific capsule by its ID.
    Args:
        capsule_id: The ID of the capsule to retrieve.
    Returns:
        Capsule object if found, None otherwise.
    """
    try:
        return Capsule.objects.get(id=capsule_id)
    except ObjectDoesNotExist:
        return None
    except Exception as e:
        print(f"An error occurred while retrieving the capsule {capsule_id}: {e}")
        return None


def get_all_capsules_for_user(owner_id):
    """
    Retrieve all capsules owned by a specific user.
    Args:
        owner_id: The ID of the UserProfile who owns the capsules.
    Returns:
        A QuerySet of Capsule objects owned by the user, or None if an error occurs.
    """
    try:
        capsules = Capsule.objects.filter(owner=owner_id)
        return capsules
    except Exception as e:
        print(f"An error occurred while retrieving capsules for user {owner_id}: {e}")
        return None


def update_capsule_by_id(capsule_id, name=None, description=None, is_public=None, unsealing_date=None):
    """
    Update an existing capsule.
    Args:
        capsule_id: The ID of the capsule to update.
        name: The new capsule name (optional)
        description: The updated capsule description (optional).
        is_public: Boolean indicating if the capsule is public (optional).
        unsealing_date: The updated date and time when the capsule will be unsealed (optional).
    Returns:
        The updated Capsule object or None if the capsule does not exist or in case of an error.
    """
    try:
        capsule = Capsule.objects.get(id=capsule_id)
        if name is not None:
            capsule.name = name
        if description is not None:
            capsule.description = description
        if is_public is not None:
            capsule.is_public = is_public
        if unsealing_date is not None:
            capsule.unsealing_date = unsealing_date
        capsule.save()
        return capsule
    except ObjectDoesNotExist:
        print(f"Capsule with id {capsule_id} does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred while updating the capsule {capsule_id}: {e}")
        return None


def delete_capsule_by_id(capsule_id):
    """
    Delete a capsule.
    Args:
        capsule_id: The ID of the capsule to delete.
    """
    try:
        capsule = Capsule.objects.get(id=capsule_id)
        capsule.delete()
        return True
    except ObjectDoesNotExist:
        print(f"Capsule with id {capsule_id} does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred while deleting the capsule {capsule_id}: {e}")
        return None
