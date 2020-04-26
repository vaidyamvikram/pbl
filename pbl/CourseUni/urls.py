from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('index',views.index,name="index"),
    path('login',views.login,name="login"),
    path('signup',views.signup,name="signup"),
    path('course',views.course,name="course"),
    path('contact',views.contact,name="contact"),
    path('category/<str:value>',views.category),
    path('logout',views.logout,name="logout"),
    path('signup_teacher',views.signup_teacher,name='signup_teacher'),
    path('myteachings',views.myteachings,name="myteachings"),
    path('confirmation/<str:val>',views.confirmation),
    path('mycourse',views.mycourse,name="mycourse"),
    path('add_to/<str:para>',views.add_to,name="add_to"),
    path('remove/<str:par>',views.remove),
    path('forgot',views.forgot,name="forgot"),
    path('otp/<str:data>/<str:ml>',views.otp,name="otp"),
    path('changepassword/<str:one>',views.changepassword,name="changepassword"),
]