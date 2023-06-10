import time
from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.


class AuthUsers(AbstractUser):
    email = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        unique=True,
    )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateField(default=date.today)
    modified_date = models.DateField(default=date.today)

    class Meta:
        verbose_name_plural = "Auth Users"
        db_table = "auth_users"

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


def blog_display_picture(instance, filename):
    filebase, extension = filename.split(".")
    return "user_profile_picture/%s.%s" % (
        str(int(round(time.time() * 1000))),
        extension,
    )


class Blog(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    user = models.ForeignKey(AuthUsers, on_delete=models.DO_NOTHING)
    display_picture = models.ImageField(
        upload_to=blog_display_picture,
        blank=True,
        null=True,
    )
