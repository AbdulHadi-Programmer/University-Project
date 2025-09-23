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


## Student Dashboard 
# @login_required
# def student_dashboard(request):
#     user = request.user

#     # Subjects for this user
#     subjects = Subject.objects.filter(semester=user.semester)

#     # Upcoming tasks
#     upcoming_tasks = Task.objects.filter(
#         user=user,
#         due_date__gte=timezone.now().date()
#     ).order_by("due_date")

#     # Learning items per subject
#     # learning_items = LearningItem.objects.filter(subject__semester=user.semester)

#     return render(request, "student_dashboard.html", {
#         "subjects": subjects,
#         "upcoming_tasks": upcoming_tasks,
#         # "learning_items": learning_items,
#     })
@login_required 
def student_dashboard(request):
    user = request.user 
    subjects = Subject.objects.filter(semester=user.semester)
    return render(request, "student_dashboard.html", {"subjects": subjects})


## Learning from Item Views: 
# 1. Learning Item List → List of learning topics for a task or subject
# 2. Learning Item Create → Add new topic
# 3. Learning Item Update → Edit Topic
# 4. Learning Item Delete → Delete Topic 

## Learning list:
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