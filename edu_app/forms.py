from django import forms
from .models import Course, Enrollment

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'category']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['progress', 'completed']