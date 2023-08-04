from django.urls import path
from account import views


urlpatterns = [
    path('register/',views.register,name='register'),
    path('signin/',views.signin,name='signin'),
    path('signin/otp-verify/<str:uid>/',views.otp_verify,name='otp-verify'),
    path('signout',views.signout,name='signout'),
]


