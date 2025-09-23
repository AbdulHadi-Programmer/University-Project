from django.contrib import admin
from .models import Subject, Task, LearningItem

# Register Subject with a simple layout
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "course_code", "std_id")  # columns in list view
    search_fields = ("name", "course_code", "std_id")  # add search box
    list_filter = ("name",)  # filter sidebar
    ordering = ("name",)  # default ordering


# Register Task with field grouping and better layout
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task_type", "subject", "user", "due_date", "created_at")
    search_fields = ("title", "task_type", "subject__name", "user__email")
    list_filter = ("task_type", "subject", "due_date")
    ordering = ("due_date",)
    fieldsets = (
        ("Task Info", {
            "fields": ("title", "task_type", "subject", "user")
        }),
        ("Dates", {
            "fields": ("due_date", "created_at", "updated_at"),
            "classes": ("collapse",)  # collapsible section
        }),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(LearningItem)
class LearningItemAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "created_at")
    search_fields = ("title", "subject__name")
    list_filter = ("subject",)