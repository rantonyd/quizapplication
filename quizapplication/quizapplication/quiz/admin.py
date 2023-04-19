from django.contrib import admin

# Register your models here.

from quiz.models import Category,Questions,Answers


class AnswerAdmin(admin.StackedInline):
    model=Answers
class QuestionAdmin(admin.ModelAdmin):
    inlines=[AnswerAdmin]


admin.site.register(Category)
admin.site.register(Questions,QuestionAdmin)
admin.site.register(Answers)