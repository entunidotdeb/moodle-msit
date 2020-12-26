import datetime
import json

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from .forms import UserUpdateForm, GeneralForm
from .models import Course, StudentRequest, Subject, Teacher, FeedbackForm, StudentQA
from .user_constants import STUDENT, TEACHER, SUB_APPROVAL, PENDING, APPROVED


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
        del form.fields['shift']
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
            if updated:
                msg = "Infos successfully updated"
            else:
                msg = "Wrong Info provided"
            messages.add_message(
                self.request, messages.INFO, _(msg)
            )
        return redirect(self.get_success_url())

    def set_student_details(self, data):
        user = self.get_object()
        student = user.student
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')
        course = data.get('course', None)
        try: 
            if course:
                course_db_obj = Course.objects.filter(course_name=int(course))
                if len(course_db_obj)>0:
                    course_db_obj_selected = course_db_obj[0]
                    student.course = course_db_obj_selected
                else:
                    #TODO
                    pass
        except Exception:
            #TODO
            pass
        enrollnum = data.get('enrollnum', -1)
        if int(enrollnum) > 0:
            student.enrollnum = int(enrollnum)
        section = data.get('section', None)
        if section:
            student.section = section
        currentyear = data.get('currentyear', None)
        currentsem = data.get('currentsem', None)
        try:
            currentyear = int(currentyear)
            currentsem = int(currentsem)
            student.currentyear = currentyear
            student.currentsem = currentsem
        except:
            #TODO
            pass
        serialnum = data.get('serialnum', None)
        if serialnum:
            student.serialnum = serialnum
        student.save()
        user.save()          
        return True

    def set_teacher_details(self, data):
        user = self.get_object()
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')
        teacher = user.teacher 
        shift = data.get('shift', None)
        if shift:
            teacher.shift = shift
        user.save()
        teacher.save()
        return True

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
    template = loader.get_template("users/subject_update.html")
    # html = "<html><body><h1>It is now %s %s.</h1></body></html>" % (now, user.email)
    return HttpResponse(template.render())


class UserSubjectsView(LoginRequiredMixin, UpdateView):
    template_name = 'users/mysubjects.html'
    model = User
    field = ['username']
    form_class = GeneralForm

    def get(self, request, **kwargs):
        form_class = GeneralForm
        form = self.get_form(form_class)
        self.object = self.get_object()
        student = getattr(self.object, 'student', None)
        enrolled_subjects, course_subjects, pending_subjects_request = list(), list(), list()
        context = dict()
        if student:
            enrolled_subjects = student.subject.all()
            course_subjects = student.course.subject_set.all().filter(
                sem=student.currentsem
            )
            pending_subjects_request = student.studentrequest_set.all().filter(status=PENDING)
        if enrolled_subjects:
            context.update({'enrolled_subjects': enrolled_subjects})
        if course_subjects:
            context.update({'course_subjects': course_subjects})
        if pending_subjects_request:
            context.update({'pending_subjects_request': pending_subjects_request})
        #TODO do smthing or remove form
        form.fields['data'].initial = "hello world"
        context.update({'form': form})
        return self.render_to_response(context)


    def get_object(self):
        return User.objects.get(username=self.request.user.username)


    def post(self, request, *args, **kwargs):
        raw_data = request.POST.get('data', '')
        student = request.user.student
        data = json.loads(raw_data)
        all_subjects = Subject.objects.all()
        all_requests = list()
        for req in data:
            request_to_teacher = None
            req_subject_id = req.get('id', None)
            req_subject = None
            if req_subject_id:
                req_subjects = all_subjects.filter(id=req_subject_id)
            if req_subjects:
                req_subject = req_subjects[0]
            subject_teachers = Teacher.objects.filter(subject__id=req_subject.id)
            subject_teacher = subject_teachers[0] if subject_teachers else None
            if subject_teacher:
                request_to_teacher = subject_teacher
            else:
                super_users = User.objects.filter(is_superuser=True)
                for super_user in super_users:
                    if getattr(super_user, "teacher", False):
                        request_to_teacher = super_user.teacher
                        break
            if req_subject and student and request_to_teacher:
                new_req = StudentRequest(
                    subject=req_subject, student=student, teacher=request_to_teacher, reqType=SUB_APPROVAL, \
                        status=PENDING
                )
                all_requests.append(new_req)
        if all_requests:
            StudentRequest.objects.bulk_create(objs=all_requests)
            msg = list()
            for req in all_requests:
                msg.append(
                    _("Requests Sent Successfully for sub ") + str(req.subject) + \
                        " to teacher " + str(req.teacher)
                )
        else:
            msg = "Requests Failed."
        messages.add_message(
                self.request, messages.INFO, msg
            )
        return redirect(self.get_success_url())


    def get_success_url(self):
        return reverse("users:subject", kwargs={"pk": self.request.user.pk})    

user_subject_view = UserSubjectsView.as_view()


class TeacherRequest(LoginRequiredMixin, UpdateView):
    template_name = 'users/myrequest.html'
    model = User
    field = ['username']
    form_class = GeneralForm

    def get(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        context = dict()
        if form:
            context.update({'form': form})
        self.object = self.get_object()
        teacher = getattr(self.object, 'teacher', None)
        teacher_requests = None
        subject_wise_requests = list()
        if teacher:
            teacher_requests = StudentRequest.objects.filter(
                teacher=teacher, reqType=SUB_APPROVAL, status=PENDING
            )
            teacher_subjects = teacher.subject.all()
        if teacher_subjects and teacher_requests:
            for subject in teacher_subjects:
                subject_wise_requests.append(
                    teacher_requests.filter(subject=subject)
                )
            context.update({'teacher_requests': subject_wise_requests, \
                'teacher_subjects': teacher_subjects})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        raw_data = request.POST.get('data', '')
        requests_to_approve = json.loads(raw_data)
        msg = ''
        for req in requests_to_approve:
            req_id = req.get('req_id', None)
            if req_id:
                req_obj = StudentRequest.objects.filter(id=req_id)
                req_obj = req_obj[0]
                student = req_obj.student
                subject = req_obj.subject
                student.subject.add(subject)
                req_obj.status = APPROVED
                req_obj.save()
                msg = msg + ", " + str(student)     
        messages.add_message(self.request, messages.INFO, "Requests of following users has been approved " + msg)
        return redirect(self.get_success_url())

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def get_success_url(self):
        return reverse("users:teacher-request", kwargs={"pk": self.request.user.pk})

user_requests_view = TeacherRequest.as_view()


class SubjectView(LoginRequiredMixin, UpdateView):
    template_name = 'users/subject.html'
    model = User
    field = ['username']
    form_class = GeneralForm
    
    def get(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        context = dict()
        self.object = self.get_object()
        return self.render_to_response(context)

# user_update_view = UserSettingsView.as_view()


class FillFeedback(LoginRequiredMixin, UpdateView):
    template_name = 'users/feedback.html'
    model = User
    field = ['username']
    form_class = GeneralForm

    def get(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        context = dict()
        self.object = self.get_object()
        student = getattr(self.object, "student", None)
        if not student:
            return self.render_to_response(context)
        subjects = student.subject.all()
        data = list()
        for subject in subjects:
            feedback = subject.feedbackform
            if feedback.is_active:
                feedback_questions = feedback.questions.all()
                data.append(
                    {
                        "subject": {
                            "id": subject.id,
                            "name": str(subject),
                            "teacher": [
                                {
                                    "id": teacher.id, "name": str(teacher)
                                } for teacher in subject.teacher.all()
                            ],
                        },
                        "question": [
                            {   "id": question.id, "desc": question.description,
                                "qtext": question.ques_text,
                                "qtype": question.ques_type,
                                "choices": [
                                    {
                                        "id": choice.id,
                                        "choice_text": choice.choice_text,
                                        "choice_val": choice.choice_val,
                                    } for choice in question.choices.all()
                                ],
                            } for question in feedback_questions
                        ]

                    }
                )
        return self.render_to_response({"data": data})

feedback_view = FillFeedback.as_view()