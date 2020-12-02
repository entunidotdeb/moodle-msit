from django.contrib.auth import get_user_model
from django.contrib.auth import forms as f
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from msitmoodle.users.models import Subject, Section
from .user_constants import COURSES, SHIFT, YEAR, SEMESTER, PROFILE_TYPE, STUDENT
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
    course = forms.ChoiceField(choices=COURSES, label='Course Enrolled', required=False)
    shift = forms.ChoiceField(choices=SHIFT, required=False)
    enrollnum = forms.IntegerField(label='Enrollment Number', required=False)
    section = forms.ModelChoiceField(queryset=Section.objects.all(), required=False)
    currentyear = forms.ChoiceField(choices=YEAR, required=False)
    currentsem = forms.ChoiceField(choices=SEMESTER, required=False)
    serialnum = forms.IntegerField(label='Class S.No.', required=False)
    profile_type = forms.ChoiceField(
        choices=PROFILE_TYPE, widget=forms.widgets.RadioSelect, label="Signing up as?",
    )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

class SocialCustomSignupForm(SocialSignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    course = forms.ChoiceField(choices=COURSES, label='Course Enrolled', required=False)
    shift = forms.ChoiceField(choices=SHIFT, required=False)
    enrollnum = forms.IntegerField(label='Enrollment Number', required=False)
    section = forms.ModelChoiceField(queryset=Section.objects.all(), required=False)
    currentyear = forms.ChoiceField(choices=YEAR, required=False)
    currentsem = forms.ChoiceField(choices=SEMESTER, required=False)
    serialnum = forms.IntegerField(label='Class S.No.', required=False)
    profile_type = forms.ChoiceField(
        choices=PROFILE_TYPE, widget=forms.widgets.RadioSelect, label="Signing up as?",
    )

    def signup(self, request, user):
        user = super(SocialCustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

class UserUpdateForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    course = forms.ChoiceField(choices=COURSES, label='Course Enrolled', required=False)
    shift = forms.ChoiceField(choices=SHIFT, required=False)
    enrollnum = forms.IntegerField(label='Enrollment Number', required=False)
    section = forms.ModelChoiceField(queryset=Section.objects.all(), required=False)
    currentyear = forms.ChoiceField(choices=YEAR, required=False)
    currentsem = forms.ChoiceField(choices=SEMESTER, required=False)
    serialnum = forms.IntegerField(label='Class S.No.', required=False)
    profile_type = forms.ChoiceField(
        choices=PROFILE_TYPE, widget=forms.widgets.HiddenInput, label="Signing up as?",
    )

class GeneralForm(forms.Form):
    data = forms.CharField(widget=forms.HiddenInput(), required=False)