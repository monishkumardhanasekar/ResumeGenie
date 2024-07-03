from django.urls import path
from .views import upload_resume, success

urlpatterns = [
    path('upload/', upload_resume, name='upload_resume'),
    path('success/', success, name='success'),
]
