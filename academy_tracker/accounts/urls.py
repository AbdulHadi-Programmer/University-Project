from django.urls import path
from .views import register_user, login_view, logout_view, profile, edit_profile, home , timetable, verify_email, resend_verification 


urlpatterns = [
    path("", home, name="home"),  # homepage
    path("register/", register_user, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    # path('timetable/', timetable, name="timetable")
    path("register/", register_user, name="register"),
    path("verify/<uuid:token>/", verify_email, name="verify_email"),
    path("resend-verification/", resend_verification, name="resend_verification"),

]