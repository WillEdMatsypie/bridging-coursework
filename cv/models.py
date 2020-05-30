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