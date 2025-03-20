# APP1/authentication.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    Authentication backend that allows login using email
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # Use email as the primary identifier
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None