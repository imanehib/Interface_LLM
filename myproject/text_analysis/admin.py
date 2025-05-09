from django.contrib import admin
from .models import SavedText, UserTyping, TypingEvent, Exercise

@admin.register(SavedText)
class SavedTextAdmin(admin.ModelAdmin):
    list_display   = ('text', 'score', 'created_at', 'updated_at')
    list_filter    = ('created_at', 'updated_at')
    list_editable = ('score',)
    search_fields = ('text',)

@admin.register(UserTyping)
class UserTypingAdmin(admin.ModelAdmin):
    list_display  = ('session_id', 'cursor_position', 'text_progression', 'created_at')
    list_filter   = ('session_id',)
    search_fields = ('session_id',)

@admin.register(TypingEvent)
class TypingEventAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'cursor_position', 'text_progression', 'timestamp')
    ordering     = ('-timestamp',)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display   = ('title', 'author', 'created_at')
    list_filter    = ('author', 'created_at')
    search_fields  = ('title', 'xml_content')
    date_hierarchy = 'created_at'
