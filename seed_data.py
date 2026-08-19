#!/usr/bin/env python
"""Script to seed sample quiz data"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from quiz.models import Category, Quiz, Question, Option

# Delete existing data
Category.objects.all().delete()
Quiz.objects.all().delete()
Question.objects.all().delete()
Option.objects.all().delete()

# Create categories
python_cat = Category.objects.create(name='Python', description='Python Programming Basics')
js_cat = Category.objects.create(name='JavaScript', description='JavaScript Programming Basics')

# Create quizzes
quiz1 = Quiz.objects.create(
    title='Python Basics',
    description='Test your Python knowledge with these basic questions',
    category=python_cat,
    difficulty='easy',
    duration=15,
    passing_score=70,
    status='active'
)

quiz2 = Quiz.objects.create(
    title='JavaScript Quiz',
    description='Test your JavaScript knowledge',
    category=js_cat,
    difficulty='medium',
    duration=20,
    passing_score=60,
    status='active'
)

# Create questions for Python quiz
q1 = Question.objects.create(
    quiz=quiz1,
    question_text='What is Python?',
    difficulty='easy',
    marks=1
)

Option.objects.create(question=q1, option_text='A programming language', is_correct=True)
Option.objects.create(question=q1, option_text='A snake', is_correct=False)
Option.objects.create(question=q1, option_text='A tool', is_correct=False)
Option.objects.create(question=q1, option_text='None of the above', is_correct=False)

q2 = Question.objects.create(
    quiz=quiz1,
    question_text='Which keyword is used to create a function in Python?',
    difficulty='easy',
    marks=1
)

Option.objects.create(question=q2, option_text='def', is_correct=True)
Option.objects.create(question=q2, option_text='function', is_correct=False)
Option.objects.create(question=q2, option_text='func', is_correct=False)
Option.objects.create(question=q2, option_text='define', is_correct=False)

# Create questions for JavaScript quiz
q3 = Question.objects.create(
    quiz=quiz2,
    question_text='What does DOM stand for?',
    difficulty='easy',
    marks=1
)

Option.objects.create(question=q3, option_text='Document Object Model', is_correct=True)
Option.objects.create(question=q3, option_text='Data Object Model', is_correct=False)
Option.objects.create(question=q3, option_text='Digital Object Model', is_correct=False)
Option.objects.create(question=q3, option_text='None', is_correct=False)

q4 = Question.objects.create(
    quiz=quiz2,
    question_text='Which method is used to add an event listener in JavaScript?',
    difficulty='easy',
    marks=1
)

Option.objects.create(question=q4, option_text='addEventListener()', is_correct=True)
Option.objects.create(question=q4, option_text='addEvent()', is_correct=False)
Option.objects.create(question=q4, option_text='onEvent()', is_correct=False)
Option.objects.create(question=q4, option_text='attachEvent()', is_correct=False)

print("✓ Sample data created successfully!")
print(f"Categories: {Category.objects.count()}")
print(f"Quizzes: {Quiz.objects.count()}")
print(f"Questions: {Question.objects.count()}")
print(f"Options: {Option.objects.count()}")
