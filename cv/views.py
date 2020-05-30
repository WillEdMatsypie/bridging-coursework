from django.shortcuts import render
from .models import Education
from .forms import EducationForm


# Create your views here.

def show_cv(request):
    education = Education.objects.all()
    return render(request, 'cv/cv.html', {'education': education})