from django.contrib.auth import get_user_model
from django.contrib.auth import forms as f
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import SignupForm
from django import forms
from msitmoodle.users.models import Subject, Section
from .user_constants import COURSES, SHIFT, YEAR, SEMESTER
User = get_user_model()


class UserChangeForm(f.UserChangeForm):
    class Meta(f.UserChangeForm.Meta):
        model = User


class UserCreationForm(f.UserCreationForm):

    error_message = f.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(f.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    course = forms.ChoiceField(choices=COURSES, label='Course Enrolled')
    shift = forms.ChoiceField(choices=SHIFT)
    enrollnum = forms.IntegerField(label='Enrollment Number')
    section = forms.ModelChoiceField(queryset=Section.objects.all())
    currentyear = forms.ChoiceField(choices=YEAR)
    currentsem = forms.ChoiceField(choices=SEMESTER)
    serialnum  = forms.IntegerField(label='Class Serial Number')
    is_cr = forms.BooleanField(help_text="Check only if you are CR", label="CR?")
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
