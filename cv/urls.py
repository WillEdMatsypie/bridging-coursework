from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_cv, name='cv'),
    path('education/new/', views.education_new, name='education_new'),
    path('education/<int:pk>/remove/', views.education_remove, name='education_remove'),
    path('skill/new/', views.skill_new, name='skill_new'),
    path('skill/<int:pk>/remove/', views.skill_remove, name='skill_remove'),
]