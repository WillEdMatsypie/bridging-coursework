from django import forms

from .models import Education

class EducationForm(forms.ModelForm):

    class Meta:
        model = Education
        fields = ('title', 'location', 'start_date', 'end_date', 'brief_text', 'detailed_text',)
        widgets = {
            'title': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Title'}),
            'location': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Location'}),
            'start_date': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Start Date'}),
            'end_date': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'End Date'}),
            'brief_text': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Brief Text...'}),
            'detailed_text': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Detailed Text...'})
         }

class SkillForm(forms.ModelForm):

    class Meta:
        model = Skill
        fields = ('title', 'skill_type',)
        widgets = {
            'title': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Title'}),
            'location': forms.ChoiceField(attrs={
            'class': 'form-control'}),
         }