from django import forms
from .models import Resume, JobDescription

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']

# ➡️ Add this new form:
class JobDescriptionForm(forms.ModelForm):
    class Meta:
        model = JobDescription
        fields = ['title', 'description_text']