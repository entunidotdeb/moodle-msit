from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
import datetime
from .forms import UserUpdateForm
from .models import Student, Teacher
from .user_constants import STUDENT, TEACHER

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    form_class = UserUpdateForm

    def get(self, request, *args, **kwargs):
        form_class = UserUpdateForm
        form = self.get_form(form_class)
        self.object = self.get_object()
        if hasattr(self.object, 'student'):
            student = self.object.student
            form = self.get_student_initials(form, student)
        elif hasattr(self.object, 'teacher'):
            teacher = self.object.teacher
            not_reqd_teacher = ['course', 'enrollnum', 'section', 'currentyear', 'currentsem', 'serialnum']
            for field in not_reqd_teacher:
                del form.fields[field]
            form = self.get_teacher_initials(form, teacher)    
        context = self.get_context_data(form=form)
        return self.render_to_response(context=context)

    def get_teacher_initials(self, form, teacher):
        form.fields['first_name'].initial = self.object.first_name
        form.fields['last_name'].initial = self.object.last_name
        form.fields['shift'].initial = teacher.shift
        form.fields['profile_type'].initial = TEACHER
        return form

    def get_student_initials(self, form, student):
        form.fields['first_name'].initial = self.object.first_name
        form.fields['last_name'].initial = self.object.last_name
        if hasattr(student, 'course'):
            course = student.course
            form.fields['course'].initial = course.course_name
        form.fields['enrollnum'].initial = student.enrollnum
        if hasattr(student, 'section'):
            form.fields['section'].initial = student.section.section
        form.fields['currentyear'].initial = student.currentyear
        form.fields['currentsem'].initial = student.currentsem
        form.fields['serialnum'].initial = student.serialnum
        form.fields['profile_type'].initial = STUDENT
        return form

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            profile_type = data.get('profile_type', None)
            updated = False
            if int(profile_type) == STUDENT:
                updated = self.set_student_details(data)
            elif int(profile_type) == TEACHER:
                updated = self.set_teacher_details(data)
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return redirect(self.get_success_url())

    def set_student_details(self, data):
        user = self.get_object()
        student = user.student
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')
        return True

    def set_teacher_details(self, data):
        return False

    
    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def current_datetime(request, username):
    now = datetime.datetime.now()
    user = User.objects.get(username=username)
    html = "<html><body><h1>It is now %s %s.</h1></body></html>" % (now, user.email)
    return HttpResponse(html)


class UserSettingsView(LoginRequiredMixin, FormView):
    template_name = 'account/user_update.html'
    form_class = UserUpdateForm

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        user = request.user

        context = self.get_context_data(form=form)
        return self.render_to_response(context)



# user_update_view = UserSettingsView.as_view()
