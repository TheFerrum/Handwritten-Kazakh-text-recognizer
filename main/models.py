from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):

    # field to store user picture
    user_avatar = models.ImageField(upload_to="user_avatars/", default='NULL')

    # returning username when called
    def __str__(self) -> str:
        return self.username