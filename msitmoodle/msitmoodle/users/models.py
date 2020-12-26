from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from .user_constants import (
    COURSES, YEAR, SEMESTER, SUBJECTS, SUB_TYPE, SHIFT, 
    FIRSTYR, FIRSTSEM, REQUESTTYPE, REQ_STATUS, QUES_TYPE
)

class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Course(models.Model):
    course_name = models.SmallIntegerField(
        choices=COURSES, verbose_name="Course Name", help_text="Course Name"
    )
    duration_year = models.SmallIntegerField(
        choices=YEAR, verbose_name="Course duration", help_text="Course duration"
    )
    duration_semester = models.SmallIntegerField(
        choices=SEMESTER, verbose_name="Semester in courses", help_text="Semester in courses"
    )

    def __str__(self):
        course_name = self.get_course_name_display()
        return '%s' % (course_name)


class Section(models.Model):
    section = models.SmallIntegerField(verbose_name="Section number")

    def __str__(self):
        return '%s' % (self.section)


class Subject(models.Model):
    """Subject and its nomenclature related stuff

    Args:
        models ([type]): [description]
    """
    year = models.SmallIntegerField(choices=YEAR, verbose_name="Year of Subject")
    sem = models.SmallIntegerField(choices=SEMESTER, verbose_name="Semester of Subject")
    name = models.CharField(verbose_name="Subject name", max_length=50)
    type = models.SmallIntegerField(choices=SUB_TYPE, verbose_name="Subject Type")
    code_prefix = models.CharField(verbose_name="Code Prefix", max_length=2)
    code_suffix = models.IntegerField(choices=SUBJECTS, verbose_name="Code Suffix")
    codenum = models.IntegerField(verbose_name="Subject Code Number")
    courses = models.ManyToManyField(
        to=Course, verbose_name="Subject of Course(s)"
    )

    def __str__(self):
        typestr = self.get_type_display()
        typestr = "(" + typestr + ")"
        return '%s' % (self.name + " " + typestr)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    enrollnum = models.BigIntegerField(verbose_name="Enrollment Number", blank=True, unique=True)
    course = models.ForeignKey(
        to=Course, verbose_name="Course Enrolled", on_delete=models.PROTECT
    )
    subject = models.ManyToManyField(
        to=Subject, verbose_name="Subjects registered",
    )
    section = models.ForeignKey(
        to=Section, on_delete=models.PROTECT, verbose_name="Section"
    )
    currentyear = models.SmallIntegerField(
        choices=YEAR, verbose_name="Course Year", help_text="Course Year", default=FIRSTYR
    )
    currentsem = models.SmallIntegerField(
        choices=SEMESTER, verbose_name="Semester", help_text="Semester", default=FIRSTSEM
    )
    serialnum = models.SmallIntegerField(
        verbose_name="Class Serial Number", help_text="Class Serial Number"
    )
    is_cr = models.BooleanField(default=False, verbose_name="CR")

    def __str__(self):
        if self.user.first_name and self.user.last_name:   
            return '%s' % (self.user.first_name + " " + self.user.last_name)
        if self.user.username:
            return '%s' % (self.user.username)
        if self.user.email:
            return '%s' % (self.user.email) 
        if self.enrollnum:
            return '%s' % (str(self.enrollnum))


class Teacher(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    shift = models.SmallIntegerField(choices=SHIFT, verbose_name="Shift")
    emp_id = models.IntegerField(verbose_name="Employee ID")
    is_proctor = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    subject = models.ManyToManyField(
        to=Subject, verbose_name="Subjects Alloted", related_name="teacher"
    )

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return '%s' % (self.user.first_name + " " + self.user.last_name)
        if self.user.username:
            return '%s' % (self.user.username)
        if self.user.email:
            return '%s' % (self.user.email) 
        if self.name:
            return '%s' % (self.name)


class StudentRequest(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(to=Teacher, on_delete=models.CASCADE)
    reqType = models.SmallIntegerField(choices=REQUESTTYPE, verbose_name="Request Type")
    status = models.SmallIntegerField(choices=REQ_STATUS, verbose_name="Request status")
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.student and self.subject:
            return '%s' % (str(self.student) + "  "  + str(self.subject))
    

class FeedbackForm(models.Model):
    subject = models.OneToOneField(to=Subject, on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Active?")

    def __str__(self):
        return "FeedBackForm: " + str(self.subject)


class Choice(models.Model):
    choice_text = models.CharField(max_length=30, null=True, blank=True)
    choice_val = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "Choice: " + (self.choice_text or str(self.choice_val))


class Question(models.Model):
    feedback = models.ForeignKey(
        to=FeedbackForm, on_delete=models.CASCADE, related_name="questions"
    )
    ques_text = models.CharField(verbose_name="Question Text", blank=False, max_length=200)
    description = models.CharField(verbose_name="Desc of question", blank=True, max_length=200)
    ques_type = models.SmallIntegerField(choices=QUES_TYPE, verbose_name="Question Type")
    choices = models.ManyToManyField(Choice, related_name="in_questions")
    right_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.ques_text)


class StudentQA(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(to=Choice, null=True, blank=True,\
         on_delete=models.PROTECT)
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE)
    answered_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.student) + " answered " + str(self.choice) + " for " + str(self.question) 
    
    class Meta:
        verbose_name = "Student's QA"
    

#TODO  create Batch model

