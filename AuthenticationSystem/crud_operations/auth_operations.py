from django.contrib.auth import get_user_model


def create_user(username, password, email):
    """
    Create a new user with the given username, email, password, first name, last name, and optional bio.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.
        email (str): The email address for the new user.

    Returns:
        The newly created user object or None if the creation failed.
    """
    User = get_user_model()
    try:
        # Correctly using create_user to handle password hashing
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        user.save()
        return user
    except Exception as e:
        print(f"An error occurred while creating the user: {e}")
        return None
