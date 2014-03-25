from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class EmailBackend( ModelBackend ):
    """
    Authenticate the user using a email instead of a username.
    Username will be randomly generated for each user at registration time.
    """
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
               return user
        except User.DoesNotExist:
            return None