from django import forms
from .models import Course, Enrollment, Question, Answer


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'category']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['progress', 'completed']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text']