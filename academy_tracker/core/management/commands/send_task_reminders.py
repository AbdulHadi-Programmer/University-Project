from django.core.management.base import BaseCommand
from django.utils import timezone
from academy.models import Task
from django.core.mail import send_mail

class Command(BaseCommand):
    help = "Send task reminders (7-day and 4-day)"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()

        tasks = Task.objects.select_related("user").all()

        for task in tasks:
            days_left = (task.due_date - today).days

            # 7 DAY REMINDER
            if days_left == 7 and not task.reminder_7_sent:
                send_mail(
                    subject=f"Reminder: {task.title} due in 7 days",
                    message=f"Your task '{task.title}' is due on {task.due_date}",
                    from_email="your@email.com",
                    recipient_list=[task.user.email],
                )
                task.reminder_7_sent = True
                task.save()

            # 4 DAY REMINDER
            if days_left == 4 and not task.reminder_4_sent:
                send_mail(
                    subject=f"Reminder: {task.title} due in 4 days",
                    message=f"Your task '{task.title}' is due on {task.due_date}",
                    from_email="your@email.com",
                    recipient_list=[task.user.email],
                )
                task.reminder_4_sent = True
                task.save()

# 0 9 * * * /Desktop/University-Project/venv/bin/python3 /Desktop/University-Project/academy_tracker/manage.py