from django.contrib import admin
from .models import blogType ,Blog
# Register your models here.
@admin.register(blogType)
class blogTypeadmin(admin.ModelAdmin):
    list_display =('id','typeName')
@admin.register(Blog)
class blogAdmin(admin.ModelAdmin):
    list_display=('id','title','blogType','author','getReadNum','createdTime','lastUpdateTime')
'''
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display=('readNum','blog')
'''