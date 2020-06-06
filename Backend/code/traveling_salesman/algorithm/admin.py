from django.contrib import admin

# Register your models here.
from .models import File, Result
admin.site.register(File)
admin.site.register(Result)

