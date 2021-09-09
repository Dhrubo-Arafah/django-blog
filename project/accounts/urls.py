from django.urls import path

from accounts import views

urlpatterns = [
    path('login/', views.login_form, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_form, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.user_update, name='update_profile'),
    path('password/', views.password_change, name='password_change '),
    path('update-profile-picture', views.update_pro_pic, name='update_pro_pic'),
]
