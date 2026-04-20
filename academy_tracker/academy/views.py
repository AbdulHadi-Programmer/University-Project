from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from .models import TimeTable, Task, LearningItem
from .forms import TimeTableForm 
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect, get_object_or_404 
from .forms import TaskForm, SubjectForm, LearningItemForm 
from .models import *
from django.utils import timezone 
from django.views.decorators.http import require_POST 
from .models import Task
#  Explicitly import ALL models used in this file
from .models import TimeTable, Task, LearningItem, Subject 
from .forms import TimeTableForm, TaskForm, SubjectForm, LearningItemForm

@login_required
def add_or_update_task(request, pk=None, subject_id=None):
    task = get_object_or_404(Task, pk=pk, user=request.user) if pk else None

    subject = None
    if subject_id:
        subject = get_object_or_404(Subject, id=subject_id, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, user=request.user, subject=subject)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user

            if subject:
                task.subject = subject  # 🔥 auto assign

            task.save()
            return redirect("student_dashboard")

    else:
        form = TaskForm(instance=task, user=request.user, subject=subject)

    return render(request, "task_form.html", {
        "form": form,
        "task_id": pk,
        "subject": subject
    })

@login_required
def task_list_all(request):
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


# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from django.db.models import Count, Q
# # from .models import Subject, Task, LearningItem

# @login_required
# def student_dashboard(request):
#     user = request.user

#     # Total :
#     tasks_count = Task.objects.filter(user=request.user).count() or 0
#     notes_count = LearningItem.objects.filter(user=request.user).count()  or 0
#     timetable_count = TimeTable.objects.filter(user=request.user).count() or 0

#     # Subjects for this user/semester, annotated with counts
#     subjects = (
#         Subject.objects
#         .filter(semester=user.semester)
#         .annotate(
#             total_tasks=Count("task", distinct=True),  # total tasks related to this subject
#             pending_tasks=Count("task", filter=Q(task__status="Pending")),
#             completed_tasks=Count("task", filter=Q(task__status="Completed")),
#             learning_items_count=Count("learning_items", distinct=True),  # uses related_name on LearningItem
#         )
#         .order_by("name", 'id')
#     )

#     # Global counts for badges / dashboard summary
#     task_pending_count = Task.objects.filter(user=user, status="Pending").count() 
#     task_completed_count = Task.objects.filter(user=user, status="Completed").count() 
#     learning_items_count = LearningItem.objects.filter(subject__semester=user.semester).count()

#     context = {
#         "subjects": subjects,
#         "task_pending_count": task_pending_count,
#         "task_completed_count": task_completed_count,
#         "learning_items_count": learning_items_count,
#         # Total Count :
#         "tasks_count": tasks_count,
#         "notes_count": notes_count,
#         "timetable_count": timetable_count,
#     }

#     return render(request, "student_dashboard.html", context)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Q

@login_required
def student_dashboard(request):
    user = request.user

    # -------------------------
    # BASIC COUNTS (user only)
    # -------------------------
    tasks_count = Task.objects.filter(user=user).count()
    notes_count = LearningItem.objects.filter(user=user).count()
    timetable_count = TimeTable.objects.filter(user=user).count()

    # -------------------------
    # SUBJECTS (ONLY USER'S)
    # -------------------------
    subjects = (
        Subject.objects
        .filter(user=user)   # ✅ FIXED: only user's subjects
        .annotate(
            total_tasks=Count("task", distinct=True),
            pending_tasks=Count(
                "task",
                filter=Q(task__status="Pending")
            ),
            completed_tasks=Count(
                "task",
                filter=Q(task__status="Completed")
            ),
            learning_items_count=Count("learning_items", distinct=True),
        )
        .order_by("name", "id")
    )

    # -------------------------
    # GLOBAL TASK STATS
    # -------------------------
    task_pending_count = Task.objects.filter(user=user, status="Pending").count()
    task_completed_count = Task.objects.filter(user=user, status="Completed").count()

    # Only count learning items belonging to this user
    learning_items_count = LearningItem.objects.filter(user=user).count()

    # -------------------------
    # CONTEXT
    # -------------------------
    context = {
        "subjects": subjects,
        "task_pending_count": task_pending_count,
        "task_completed_count": task_completed_count,
        "learning_items_count": learning_items_count,
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
# =====================================================================================================================================================
# =====================================================================================================================================================
# =====================================================================================================================================================
# @login_required
# def add_or_update__subject(request, pk=None):
#     subject = Subject.objects.filter(pk=pk, user= request.user) if pk else None 
#     if request.method == "POST":
#         form = SubjectForm(request.POST, instance=subject, user=request.user)
#         if form.is_valid():
#             subject = form.save(commit=False)
#             subject.user = request.user
#             subject.save()
#             return redirect("student_dashboard")
#     else :
#         form = SubjectForm(instance=subject, user=request.user)
    
#     return render(request, "subject_form.html", {"form": form})
from django.contrib import messages

@login_required
def add_or_update__subject(request, pk=None):
    # Existing subject ko fetch karo (sirf current user ka)
    # subject = Subject.objects.filter(pk=pk, user=request.user).first() if pk else None
    subject = get_object_or_404(Subject, pk=pk, user=request.user) if pk else None

    print("PK:", pk)
    # print("PK:", pk)
    print("User:", request.user)
    print("All subjects of user:", Subject.objects.filter(user=request.user))
    print("Matching subject:", Subject.objects.filter(pk=pk, user=request.user))

    print("request.user.id:", request.user.id)
    print("request.user:", request.user)
    print("Subjects:", Subject.objects.values('id', 'user'))

    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject, user=request.user)
        
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.semester = request.user.semester   # Safety ke liye again set kar rahe hain
            subject.save()
            
            messages.success(request, "Subject saved successfully!")
            return redirect("student_dashboard")
    
    else:
        form = SubjectForm(instance=subject, user=request.user)
    
    return render(request, "subject_form.html", {"form": form, "subject": subject})


@login_required
def delete_item(request, pk):
    item = get_object_or_404(LearningItem, pk=pk, user=request.user)
    if request.method == "POST":
        item.delete()
        return redirect("student_dashboard")  # use correct URL name
    return redirect("student_dashboard")



@login_required
def task_list_by_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, semester=request.user.semester)
    tasks = Task.objects.filter(subject=subject, user=request.user).order_by("due_date")
    return render(request, "tasks.html", {
        "subject": subject,
        "tasks": tasks
    }) 


# @login_required 
# def

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

# def subject_delete(request, pk):
#     subject = get_object_or_404(Subject, pk=pk, user=request.user)
#     subject.delete()
#     return redirect('student_dashboard')


def subject_delete(request, pk):
    if request.method == "POST":
        Subject.objects.filter(id=pk, user=request.user).delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)