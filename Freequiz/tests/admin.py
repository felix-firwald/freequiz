from django.contrib import admin
from .models import (
    Variant,
    BlueprintQuestion,
    Question,
    BlueprintTest,
    Result,
)


class VariantInline(admin.StackedInline):
    model = Variant


class BlueprintQuestionAdmin(admin.ModelAdmin):
    inlines = [VariantInline]


class BprQuesInline(admin.StackedInline):
    model = BlueprintQuestion


class BprTestAdmin(admin.ModelAdmin):
    inlines = [BprQuesInline]


admin.site.register(BlueprintQuestion, BlueprintQuestionAdmin)
admin.site.register(BlueprintTest, BprTestAdmin)

for model in (
    Variant, Question, Result
):
    admin.site.register(model)
