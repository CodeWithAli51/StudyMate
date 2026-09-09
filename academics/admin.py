from django.contrib import admin

from .models import Subject, Chapter, Topic


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'order')
    search_fields = ('name', 'code')
    ordering = ('order', 'name')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'number', 'order')
    list_filter = ('subject',)
    search_fields = ('name', 'subject__name')
    ordering = ('subject', 'order', 'number', 'name')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter', 'order')
    list_filter = ('chapter__subject', 'chapter')
    search_fields = ('name', 'chapter__name')
    ordering = ('chapter', 'order', 'name')
