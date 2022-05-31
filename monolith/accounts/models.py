from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    The User model is someone that logs in to administer the
    conference application, not someone that is attending or
    presenting at the conference.

    The custom user model for this project as advised by Django docs
    https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
    """
