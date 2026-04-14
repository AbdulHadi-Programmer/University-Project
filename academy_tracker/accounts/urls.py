from django.urls import path
from . import views 


urlpatterns = [
    path('',           views.home,          name='home'),
    path('register/',  views.register_user,  name='register'),
    path('login/',     views.login_view,     name='login'),
    path('logout/',    views.logout_view,    name='logout'),
    path('verify-otp/',views.verify_otp,     name='verify_otp'),
    path('resend-otp/',views.resend_otp,     name='resend_otp'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile', views.profile, name='profile'),

]
 