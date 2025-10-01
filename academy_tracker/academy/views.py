from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect, get_object_or_404 
from .forms import TaskForm, SubjectForm, LearningItemForm 
from .models import *
from django.utils import timezone 
from django.views.decorators.http import require_POST 



## Task Model CRUD :
# @login_required
# def add_or_update_task(request, pk=None):
#     # Check if a primary key (pk) is provided in the URL
#     if pk:
#         # If pk exists, retrieve the existing task object
#         task = get_object_or_404(Task, pk=pk, user=request.user)
#     else:
#         # If no pk, initialize a new, empty task object
#         task = None

#     if request.method == "POST":
#         # If a task object exists, pass it to the form for updating
#         form = TaskForm(request.POST, instance=task, user=request.user)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.user = request.user
#             task.save()
#             return redirect("task_list")
#     else:
#         # For a GET request, create a form instance
#         # If a task object exists, the form will be pre-filled with its data
#         form = TaskForm(instance=task, user=request.user)

#     context = {
#         "form": form,
#         "task_id": pk # Optional: for potential use in the template
#     }
#     return render(request, "task_form.html", context)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

@login_required
def add_or_update_task(request, pk=None):
    task = get_object_or_404(Task, pk=pk, user=request.user) if pk else None

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("student_dashboard")  # better redirect here
    else:
        form = TaskForm(instance=task, user=request.user)

    context = {
        "form": form,
        "task_id": pk,
    }
    return render(request, "task_form.html", context)


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "task_list.html", {"tasks": tasks})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("student_dashboard")  # use correct URL name
    return redirect("student_dashboard")

@login_required
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == "POST": 
        subject.delete()
        return redirect("student_dashboard")
    return redirect("student_dashboard")


# Old View :
# @login_required
# def student_dashboard(request):
#     user = request.user  

#     # Prepare all data in one context dict
#     context = {
#         "task_pending_count": Task.objects.filter(user=user, status="Pending").count(),
#         "task_completed_count": Task.objects.filter(user=user, status="Completed").count(),
#         "learning_items_count": LearningItem.objects.filter(subject__semester=user.semester).count(),
#         "subjects": Subject.objects.filter(semester=user.semester),
#     }

#     return render(request, "student_dashboard.html", context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Q
from .models import Subject, Task, LearningItem

@login_required
def student_dashboard(request):
    user = request.user

    # Total :
    tasks_count = Task.objects.filter(user=request.user).count() or 0
    notes_count = LearningItem.objects.filter(user=request.user).count()  or 0
    timetable_count = TimeTable.objects.filter(user=request.user).count() or 0

    # Subjects for this user/semester, annotated with counts
    subjects = (
        Subject.objects
        .filter(semester=user.semester)
        .annotate(
            total_tasks=Count("task", distinct=True),  # total tasks related to this subject
            pending_tasks=Count("task", filter=Q(task__status="Pending")),
            completed_tasks=Count("task", filter=Q(task__status="Completed")),
            learning_items_count=Count("learning_items", distinct=True),  # uses related_name on LearningItem
        )
        .order_by("name")
    )

    # Global counts for badges / dashboard summary
    task_pending_count = Task.objects.filter(user=user, status="Pending").count() 
    task_completed_count = Task.objects.filter(user=user, status="Completed").count() 
    learning_items_count = LearningItem.objects.filter(subject__semester=user.semester).count()

    context = {
        "subjects": subjects,
        "task_pending_count": task_pending_count,
        "task_completed_count": task_completed_count,
        "learning_items_count": learning_items_count,
        # Total Count :
        "tasks_count": tasks_count,
        "notes_count": notes_count,
        "timetable_count": timetable_count,
    }

    return render(request, "student_dashboard.html", context)


## Learning list:
@login_required
def learning(request):
    user = request.user
    learning_items = LearningItem.objects.filter(subject__semester=user.semester)
    return render(request, "learning_item.html", {"learn": learning_items })


@login_required
def learning_item_list(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, semester=request.user.semester)
    learning_items = LearningItem.objects.filter(subject=subject, user=request.user)
    return render(request, "learning_items.html", {
        "subject": subject,
        "learning_items": learning_items
    })


@login_required
def add_or_update_learningItem(request, pk=None):
    item = LearningItem.objects.filter(pk=pk, user=request.user).first() if pk else None

    if request.method == "POST":
        form = LearningItemForm(request.POST, instance=item, user=request.user)
        if form.is_valid():
            learning_item = form.save(commit=False)
            learning_item.user = request.user  # link user automatically
            learning_item.save()
            return redirect("student_dashboard")
    else:
        form = LearningItemForm(instance=item, user=request.user)

    return render(request, "learning_form.html", {"form": form})

## Subject CRUD : 
# Create New Subject :
@login_required
def add_or_update__subject(request, pk=None):
    subject = Subject.objects.filter(pk=pk, user= request.user) if pk else None 
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject, user=request.user)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect("student_dashboard")
    else :
        form = SubjectForm(instance=subject, user=request.user)
    
    return render(request, "subject_form.html", {"form": form})




@login_required
def delete_item(request, pk):
    item = get_object_or_404(LearningItem, pk=pk, user=request.user)
    if request.method == "POST":
        item.delete()
        return redirect("student_dashboard")  # use correct URL name
    return redirect("student_dashboard")



@login_required
def task_list(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, semester=request.user.semester)
    tasks = Task.objects.filter(subject=subject, user=request.user).order_by("due_date")
    return render(request, "tasks.html", {
        "subject": subject,
        "tasks": tasks
    }) 


# @login_required 
# def
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from .models import TimeTable 
from .forms import TimeTableForm 

# List View 
# @login_required 
# def timetable_list(request):
#     timetables = TimeTable.objects.filter(user=request.user).order_by("day", "start_time")
#     return render(request, "timetable_list.html", {"timetables": timetables})
from django.db.models import Case, When, Value, IntegerField
import datetime 

@login_required
def timetable_list(request):
    # Current Day ka name (e.g: "Monday")
    current_day = datetime.datetime.today().strftime("%A")
    day_order = Case(
        When(day="Monday", then=Value(1)),
        When(day="Tuesday", then=Value(2)),
        When(day="Wednesday", then=Value(3)),
        When(day="Thursday", then=Value(4)),
        When(day="Friday", then=Value(5)),
        When(day="Saturday", then=Value(6)),
        When(day="Sunday", then=Value(7)),
        output_field=IntegerField(),
    )

    timetables = TimeTable.objects.filter(user=request.user).order_by(day_order, "start_time")

    return render(request, "timetable_list.html", {"timetables": timetables, "current_day": current_day})



# CREATE view
@login_required
def timetable_create(request):
    if request.method == "POST":
        form = TimeTableForm(request.POST, user=request.user)
        if form.is_valid():
            timetable = form.save(commit=False)
            timetable.user = request.user
            timetable.save()
            return redirect("timetable_list")
    else:
        form = TimeTableForm(user=request.user)
    return render(request, "timetable_form.html", {"form": form})


# UPDATE view
@login_required
def timetable_update(request, pk):
    timetable = get_object_or_404(TimeTable, pk=pk, user=request.user)
    if request.method == "POST":
        form = TimeTableForm(request.POST, instance=timetable, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("timetable_list")
    else:
        form = TimeTableForm(instance=timetable, user=request.user)
    return render(request, "timetable_form.html", {"form": form})


# DELETE view  (remove the confirmation view and add direct)
@login_required
def timetable_delete(request, pk):
    timetable = get_object_or_404(TimeTable, pk=pk, user=request.user)
    timetable.delete()
    return redirect("timetable_list")

