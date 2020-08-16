"""accounts.mdels.py"""
import uuid

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from moodle.users.models import User

class Student(models.Model):
    """Model for students

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    enrollment_id = models.UUIDField(verbose_name="enrollment number", default=uuid.uuid4)
    num_of_courses_enrolled = models.IntegerField()


class Teacher(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
