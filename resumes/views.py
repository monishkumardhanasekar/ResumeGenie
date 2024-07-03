from django.shortcuts import render, redirect
from .forms import ResumeUploadForm

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ResumeUploadForm()
    return render(request, 'upload_resume.html', {'form': form})

def success(request):
    return render(request, 'success.html')
