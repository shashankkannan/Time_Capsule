from django.urls import path
from . import views
from .views import (
    PasswordResetView,
    PasswordResetDoneView,
    CustomPasswordResetConfirmView,
    PasswordResetCompleteView,
)

app_name = 'AuthenticationSystem'
urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_signup, name='user_signup'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.update_profile_picture, name='update_profile_picture'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('check-username-availability/', views.check_username_availability, name='check_username_availability'),
    path('verify_email/<str:verification_token>/', views.verify_email, name='verify_email'),
    path('update_user_history', views.update_user_history, name='update_user_history'),
]
