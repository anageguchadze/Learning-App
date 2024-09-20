from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
class Course(models.Model):
    CATEGORY_CHOICES = [
        ('math', 'Mathematics'),
        ('science', 'Science'),
        ('history', 'History'),
        ('tech', 'Technology'),
    ]
    
    instructor = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'instructor'})
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
    
class Enrollment(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)  # Percentage of completion
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name} - {'Completed' if self.completed else 'In Progress'}"
    
class Question(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, null=True, blank=True)
    question_text = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question_text[:50])
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'instructor'}, null=True, blank=True)  # Make it nullable
    answer_text = models.TextField()
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question.slug}"

