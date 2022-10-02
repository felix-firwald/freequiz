from django.contrib import admin
from .models import (
    Variant,
    Question,
    Test,
    Result
)

admin.site.register(Variant)
admin.site.register(Question)
admin.site.register(Test)
admin.site.register(Result)
