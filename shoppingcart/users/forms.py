from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from users.models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
