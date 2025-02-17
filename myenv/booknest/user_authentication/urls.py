from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_view, name='signup_page'),
    path('login/', views.login_view, name='login_page'),
    path('home/', views.home_view, name = 'home_page' ),
    path('signout/', views.signout_view, name = 'signout' ),
    path('forgetPassword/', views.forgetPassword_view, name='forgetPassword_page'),
    path('otpSignup/', views.otpSignup_view, name='otp_page'),
    path('reEnterPassword', views.reEnterPassword_view, name='reEnterPassword_page'),
    
]
#HardPass123