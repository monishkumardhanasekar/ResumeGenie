from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),
    path('success/', views.success, name='success'),
    path('upload_job/', views.upload_job_description, name='upload_job'),
    path('upload_job_success/', views.upload_job_success, name='upload_job_success'),
    path('match_resume_job/', views.match_resume_to_job, name='match_resume_job'),
]
