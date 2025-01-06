from django.contrib import admin
from . import models


class FaqAdmin(admin.StackedInline):
    model = models.Faq


class VideoAdmin(admin.StackedInline):
    model = models.Video


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'created_at']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'title', 'duration', 'video_count', 'price', 'discount', 'is_paid', 'level',
                    'created_at', 'is_recommended', 'course_status', 'status']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_recommended', 'course_status', 'status']
    list_filter = ['status', 'category']
    search_fields = ['title']
    inlines = [FaqAdmin]


@admin.register(models.Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'order', 'created_at']
    inlines = [VideoAdmin]


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['course', 'body', 'parent', 'created_at', 'status']
    list_editable = ['status']
