from TimeCapsuleManagement.models import CapsuleContent
from django.core.exceptions import ObjectDoesNotExist


def create_capsule_content(file_type, file, capsule_id):
    """
    Create a new capsule content.
    Args:
        file_type: Type of the file (e.g., photo, video, text).
        file: The file object to be uploaded.
        capsule_id: The ID of the capsule associated with the content.
    Returns:
        The newly created CapsuleContent object.
    """
    try:
        capsule_content = CapsuleContent.objects.create(
            file_type=file_type,
            file=file,
            capsule_id=capsule_id
        )
        return capsule_content
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while creating capsule content: {e}")
        return None


def get_capsule_content_by_id(content_id):
    """
    Retrieve a specific capsule content by its ID.
    Args:
        content_id: The ID of the capsule content to retrieve.
    Returns:
        CapsuleContent object if found, None otherwise.
    """
    try:
        return CapsuleContent.objects.get(id=content_id)
    except ObjectDoesNotExist:
        return None
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while retrieving capsule content {content_id}: {e}")
        return None


def get_capsule_content_for_capsule(capsule_id):
    """
    Retrieve all capsule content associated with a specific capsule.
    Args:
        capsule_id: The ID of the capsule.
    Returns:
        QuerySet of CapsuleContent objects related to the specified capsule.
    """
    try:
        return CapsuleContent.objects.filter(capsule_id=capsule_id)
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while retrieving capsule content for capsule {capsule_id}: {e}")
        return None


def update_capsule_content_by_id(content_id, file_type=None, file=None, capsule_id=None):
    """
    Update an existing capsule content.
    Args:
        content_id: The ID of the capsule content to update.
        file_type: Type of the file (e.g., photo, video, text).
        file: The updated file object.
        capsule_id: The updated ID of the capsule associated with the content.
    Returns:
        The updated CapsuleContent object.
    """
    try:
        capsule_content = CapsuleContent.objects.get(id=content_id)
        if file_type is not None:
            capsule_content.file_type = file_type
        if file is not None:
            capsule_content.file = file
        if capsule_id is not None:
            capsule_content.capsule_id = capsule_id
        capsule_content.save()
        return capsule_content
    except ObjectDoesNotExist:
        return None
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while updating capsule content {content_id}: {e}")
        return None


def delete_capsule_content_by_id(content_id):
    """
    Delete a capsule content.
    Args:
        content_id: The ID of the capsule content to delete.
    """
    try:
        capsule_content = CapsuleContent.objects.get(id=content_id)
        capsule_content.delete()
        return True
    except ObjectDoesNotExist:
        return None
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while deleting capsule content {content_id}: {e}")
        return None
