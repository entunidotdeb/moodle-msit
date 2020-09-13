from django.urls import path

from msitmoodle.users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
    current_datetime,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("<str:username>/current_datetime", view=current_datetime, name="mysuccess"),
]
