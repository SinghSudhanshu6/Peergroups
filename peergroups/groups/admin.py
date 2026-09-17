from django.contrib import admin
from .models import Group, Membership, Comment, Photo


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'interest', 'location', 'meeting_time', 'creator', 'member_count')
    list_filter = ('interest',)
    search_fields = ('name', 'description', 'location')
    inlines = [MembershipInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('group', 'author', 'created_at')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('group', 'uploader', 'uploaded_at')
