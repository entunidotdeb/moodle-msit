from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html

from msitmoodle.users.forms import UserChangeForm, UserCreationForm
from .models import Course, Section, Subject, Student, Teacher

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ("course_name__startswith",)
    readonly_fields = ('subjects',)
    fields = ("course_name", "duration_year", "duration_semester", "subjects", )

    def subjects(self, obj):
        subject_list = '<ul>'
        subject_queryset = obj.subject_set.all()
        for subject in subject_queryset:
            litem = '<li>{}</li>'.format(subject)
            subject_list += litem
        subject_list += '</ul>'
        return format_html(subject_list)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ("name__startswith",)
    list_filter = ("year", "sem", "courses", "type")
    filter_horizontal = ()
    

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ("enrollnum",)
    list_display = ("name", "enrollnum")
    list_filter = ("course", "currentyear", "is_cr")

    def name(self, obj):
        return obj

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    search_fields = ("user",)
    list_display = ("name", "email", )
    list_filter = ("shift",)

    def name(self, obj):
        return obj
    
    def email(self, obj):
        return obj.user.email
    