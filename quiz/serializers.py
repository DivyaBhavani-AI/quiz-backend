from rest_framework import serializers
from .models import Category, Quiz, Question, Option, Attempt, Answer, UserProfile
from django.contrib.auth.models import User
from .models import UserProfile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Quiz
        fields = '__all__'
    
class QuestionSerializer(serializers.ModelSerializer):
    quiz= QuizSerializer(read_only=True)
    class Meta:
        model = Question
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

