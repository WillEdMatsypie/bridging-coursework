
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from .models import Education, Skill, Experience, Interest
from .forms import EducationForm, SkillForm, ExperienceForm, InterestForm


# Create your views here.

def show_cv(request):
    education = Education.objects.all()
    tech_skills = Skill.objects.filter(skill_type__exact="technical")
    other_skills = Skill.objects.filter(skill_type__exact="other")
    experience = Experience.objects.all()
    return render(request, 'cv/cv.html', {'education': education, 'tech_skills':tech_skills, 'other_skills':other_skills, 'experience':experience})

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

@login_required
def experience_new(request):
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.save()
            return redirect('cv')
    else:
        form = ExperienceForm()
    return render(request, 'cv/experience_edit.html', {'form': form})

@login_required
def experience_remove(request, pk):
    item = get_object_or_404(Experience, pk=pk)
    item.delete()
    return redirect('/cv/')

@login_required
def interest_new(request):
    if request.method == "POST":
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.save()
            return redirect('cv')
    else:
        form = InterestForm()
    return render(request, 'cv/interest_edit.html', {'form': form})

@login_required
def interest_remove(request, pk):
    item = get_object_or_404(Interest, pk=pk)
    item.delete()
    return redirect('/cv/')