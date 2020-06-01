from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_cv, name='cv'),
    path('education/new/', views.education_new, name='education_new'),
    path('education/<int:pk>/remove/', views.education_remove, name='education_remove'),
    path('skill/new/', views.skill_new, name='skill_new'),
    path('skill/<int:pk>/remove/', views.skill_remove, name='skill_remove'),
    path('experience/new/', views.experience_new, name='experience_new'),
    path('experience/<int:pk>/remove/', views.experience_remove, name='experience_remove'),
    path('interest/new/', views.interest_new, name='interest_new'),
    path('interest/<int:pk>/remove/', views.interest_remove, name='interest_remove'),
]