from django.contrib import admin
from messenger.models import *


@admin.register(Message, BlackList)
class PersonAdmin(admin.ModelAdmin):
    pass
# Register your models here.
