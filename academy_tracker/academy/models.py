from django.db import models
from django.conf import settings 

SEMESTER_CHOICES = [(i, f"Semester {i}") for i in range(1, 9)]

class Subject(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        help_text="Assign to a specific user (optional)"
    )
    name = models.CharField(max_length=50)
    course_code = models.CharField(max_length=20, null=True, blank=True)
    std_id = models.CharField(max_length=15, default="BSE-25S-006")
    semester = models.IntegerField(choices=SEMESTER_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    TASK_TYPES = [
        ('Assignment', "Assignment"),
        ('Quiz', "Quiz"),
        ('Project', "Project"),
        ('Mid_Term', "Mid Term Exam"),
        ('Final_Term', "Final Term Exam")
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    task_type = models.CharField(max_length=20, choices=TASK_TYPES, default="Assignment")
    due_date = models.DateField()
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("On Going", "On Going")
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.task_type})"


class LearningItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="learning_items")
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.subject.name})"


class TimeTable(models.Model):
    DAYS_OF_WEEK = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
        ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    day = models.CharField(max_length=20, choices = DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.ForeignKey(Subject, on_delete= models.CASCADE)
    room_no = models.CharField(max_length=100, blank=True, null=True)

