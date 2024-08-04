from . import views
from .views import Index
from django.urls import path

app_name = 'TimeCapsuleManagement'
urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('my-capsules/', views.my_capsules, name='my_capsules'),
    path('edit/<int:capsule_id>/', views.edit_capsule, name='edit_capsule'),
    path('capsule-contents/<int:capsule_id>/', views.get_capsule_contents, name='get_capsule_contents'),
    path('delete/<int:capsule_id>/', views.delete_capsule, name='delete_capsule'),
    path('post_comment/<int:capsule_id>/', views.post_comment, name='post_comment')
]