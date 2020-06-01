from django.db import models

# Create your models here.

class Education(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_date = models.CharField(max_length=20)
    end_date = models.CharField(max_length=20)
    brief_text = models.CharField(max_length=200) 
    detailed_text = models.TextField()

    def __str__(self):
        return self.title

class Skill(models.Model):
    TYPE_CHOICES = (
    ('technical','TECHNICAL'),
    ('other', 'OTHER'),
    )
    title = models.CharField(max_length=200)
    skill_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='technical')

    def __str__(self):
        return self.title + " " + self.skill_type

class Experience(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title