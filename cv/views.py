
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from .models import Education, Skill
from .forms import EducationForm, SkillForm


# Create your views here.

def show_cv(request):
    education = Education.objects.all()
    tech_skills = Skill.objects.filter(skill_type__exact="technical")
    other_skills = Skill.objects.filter(skill_type__exact="other")
    return render(request, 'cv/cv.html', {'education': education, 'tech_skills':tech_skills, 'other_skills':other_skills})

@login_required
def education_new(request):
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.save()
            return redirect('cv')
    else:
        form = EducationForm()
    return render(request, 'cv/education_edit.html', {'form': form})

@login_required
def education_remove(request, pk):
    item = get_object_or_404(Education, pk=pk)
    item.delete()
    return redirect('/cv/')


@login_required
def skill_new(request):
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.save()
            return redirect('cv')
    else:
        form = SkillForm()
    return render(request, 'cv/skill_edit.html', {'form': form})

@login_required
def skill_remove(request, pk):
    item = get_object_or_404(Skill, pk=pk)
    item.delete()
    return redirect('/cv/')