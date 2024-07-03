from django.contrib import admin

# Register your models here.

from .models import *

@admin.register(Risks)
class RisksAdmin(admin.ModelAdmin):
    list_display = ('id', 'risk_type')

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'risks', 'question_text')

@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ('id', 'questions', 'answer_text', 'prob_happen', 'prob_nothappen')

@admin.register(UserResponses)
class UserResponsesAdmin(admin.ModelAdmin):
    list_display = ('id', 'questions', 'answers', 'response_date')
