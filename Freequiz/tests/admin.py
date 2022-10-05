from django.contrib import admin
from .models import (
    Variant,
    BlueprintQuestion,
    Question,
    BlueprintTest,
    Test,
)

for model in (
    Variant, BlueprintQuestion,
    Question, BlueprintTest, Test
):
    admin.site.register(model)
