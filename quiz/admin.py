from django.contrib import admin
from .models import Category, Quiz, UserProfile, Question, Option, Attempt, Answer


admin.site.register(Category)
admin.site.register(Quiz)
admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Attempt)
admin.site.register(Answer)