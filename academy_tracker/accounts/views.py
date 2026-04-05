from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SignupForm, LoginForm, ProfileEditForm


# 🔥 SIGNUP (Direct — no email nonsense)
def register_user(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            # auto login after signup
            login(request, user)

            return redirect("student_dashboard")
    else:
        form = SignupForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    form = LoginForm()  # ✅ always exists

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )

            if user:
                login(request, user)
                return redirect("student_dashboard")

            form.add_error(None, "Invalid email or password")

    return render(request, "login.html", {"form": form})


# 🔥 LOGOUT
def logout_view(request):
    logout(request)
    return redirect("home")

#  Explicitly import ALL models used in this file
from academy.models import TimeTable, Task, LearningItem, Subject 
from academy.forms import TimeTableForm, TaskForm, SubjectForm, LearningItemForm
# from academy.views import 
# 🔥 PROFILE VIEW
@login_required
def profile(request):
    # subject_count = Subject.objects.filter(user=user)
    total_tasks = Task.objects.filter(user=request.user).count() or 0
    notes_count = LearningItem.objects.filter(user=request.user).count()  or 0
    subjects_count = Subject.objects.filter(user=request.user).count() or 0

    return render(request, "profile.html", {"user": request.user, "total_tasks": total_tasks, "learning_items_count": notes_count, "subjects_count": subjects_count})


# 🔥 EDIT PROFILE
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("profile")
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, "edit_profile.html", {"form": form})


# 🔥 HOME
def home(request):
    return render(request, "home.html")


# 🔥 TIMETABLE (unchanged — it's fine)
