from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest
from msitmoodle.users.models import Teacher, Course, Section, Student
from .user_constants import (
    TEACHER,
    PROCTOR,
    HOD,
    STUDENT,
    CR,
)


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def save_teacher(self, user, data):
        shift = data.get('shift', 1)
        employee_id = data.get('emp_id', 1)
        teacher_obj = Teacher(user=user, shift=shift, emp_id=employee_id)
        teacher_obj.save()
    
    def save_student(self, user, data):
        enrollnum = data.get('enrollnum', int(0))
        course = data.get('course', int(1))
        serialnum = data.get('serialnum', int(1))
        course = Course.objects.filter(course_name=int(course))
        if len(course) > 0: 
            course = course[0]
        section = Section.objects.all()[0]
        #TODO do similar for section
        student_obj = Student(
            user=user,
            enrollnum=enrollnum,
            course=course,
            serialnum=serialnum,
            section=section,
        )
        student_obj.save()
    
    def save_user(self, request, user, form, commit=False):
        user = super(AccountAdapter, self).save_user(
            request, user, form, commit
        )
        user.save()
        data = form.cleaned_data
        if 'profile_type' in data and data['profile_type']:
            profile_type = int(data.get('profile_type'))
            if profile_type == TEACHER:
                self.save_teacher(user, data)
            elif profile_type == STUDENT:
                self.save_student(user, data)
        return user  

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def save_user(self, request, sociallogin, form):
        user = super(SocialAccountAdapter, self).save_user(
            request, sociallogin, form
        )
        user.save()
        return user