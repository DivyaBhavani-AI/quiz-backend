from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=50, choices=[('easy','Easy'),('medium','Medium')])
    duration = models.IntegerField(choices=[(10,'10 minutes'),(15,'15 minutes')])
    passing_score = models.IntegerField(choices=[(60, '60%'),(70, '70%'),(80, '80%')])    
    status = models.CharField(max_length=50, choices=[('active','Active'),('inactive','Inactive')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[('admin','Admin'),('student','Student')])
    status = models.CharField(max_length=30, choices=[('active','Active'),('inactive','Inactive')], default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text=models.TextField(max_length=500)
    marks = models.IntegerField(default=1)
    explanation = models.TextField(blank=True, null=True)
    difficulty=models.CharField(max_length=50,choices=[('easy','Easy'),('medium','Medium')])
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

class Option(models.Model): 
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text


class Attempt(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    correct_answer = models.IntegerField(default=0)
    incorrect_answer = models.IntegerField(default=0)
    unanswered = models.IntegerField(default=0)
    time_taken = models.DurationField(blank=True, null=True)
    status=models.CharField(max_length=30,choices=[('completed', 'Completed'),('inprogress','In Progress')])
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"attempt by {self.user.username} for quiz {self.quiz.title}"


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"answer by {self.user.username} for question {self.question.id}"

