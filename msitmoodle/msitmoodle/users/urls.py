from django.urls import path
from django.views.generic import TemplateView

from msitmoodle.users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
    user_subject_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("~subject/<int:pk>/", view=user_subject_view, name="subject"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]