import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    @property
    def is_teacher(self):
        return self.is_teacher

    @property
    def is_student(self):
        return self.is_student    

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})