from django.urls import path,include
from . import views
from django.contrib import admin


urlpatterns = [ 
    path('', views.welcome, name='welcome'),
    path('dashboard/', views.user_dashboard, name='api-dashboard'),
    path('get-categories/', views.get_categories, name='get-categories'),
    path('get-categories/<int:pk>/', views.get_categories),
    path('get-quizzes/', views.get_quizzes, name='get-quizzes'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit-quiz'),
    path('get-questions/', views.get_questions),
    path('get-questions/<int:quiz_id>/', views.get_questions),
    path('get-options/', views.get_option),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    
]