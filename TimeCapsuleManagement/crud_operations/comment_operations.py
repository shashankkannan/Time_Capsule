from TimeCapsuleManagement.models import Comment
from django.core.exceptions import ObjectDoesNotExist


def create_comment(user_id, capsule_id, content):
    """
    Create a new comment.
    Args:
        user_id: The user who is creating the comment.
        capsule_id: The ID of the capsule the comment belongs to.
        content: The content of the comment.
    Returns:
        The newly created Comment object.
    """
    try:
        comment = Comment.objects.create(
            user=user_id,
            capsule_id=capsule_id,
            content=content
        )
        return comment
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while creating a comment: {e}")
        return None


def get_comment_by_id(comment_id):
    """
    Retrieve a specific comment by its ID.
    Args:
        comment_id: The ID of the comment to retrieve.
    Returns:
        Comment object if found, None otherwise.
    """
    try:
        return Comment.objects.get(id=comment_id)
    except ObjectDoesNotExist:
        return None
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while retrieving comment {comment_id}: {e}")
        return None


def get_comments_for_capsule(capsule_id):
    """
    Retrieve all comments associated with a specific capsule.
    Args:
        capsule_id: The ID of the capsule.
    Returns:
        QuerySet of Comment objects related to the specified capsule.
    """
    try:
        return Comment.objects.filter(capsule_id=capsule_id)
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while retrieving comments for capsule {capsule_id}: {e}")
        return None


def update_comment_by_id(comment_id, content):
    """
    Update an existing comment.
    Args:
        comment_id: The ID of the comment to be updated.
        content: The new content for the comment.
    Returns:
        The updated Comment object.
    """
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.content = content
        comment.save()
        return comment
    except ObjectDoesNotExist:
        return None
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while updating comment {comment_id}: {e}")
        return None


def delete_comment_by_id(comment_id):
    """
    Delete a comment.
    Args:
        comment_id: The ID of the comment to be deleted.
    """
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return True
    except ObjectDoesNotExist:
        return None
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while deleting comment {comment_id}: {e}")
        return None
