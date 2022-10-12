from django.contrib import admin
from .models import (
    Variant,
    Question,
    Test,
    Result,
)


class VariantInline(admin.StackedInline):
    model = Variant


class QuestionAdmin(admin.ModelAdmin):
    inlines = [VariantInline]


class QuesInline(admin.StackedInline):
    model = Question


class TestAdmin(admin.ModelAdmin):
    inlines = [QuesInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)

for model in (
    Variant, Result
):
    admin.site.register(model)
