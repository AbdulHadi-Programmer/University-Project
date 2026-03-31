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


# 🔥 PROFILE VIEW
@login_required
def profile(request):
    return render(request, "profile.html", {"user": request.user})


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
from datetime import datetime

def timetable(request):
    current_day = datetime.now().strftime('%A')

    day_icons = {
        "Monday": "🌞",
        "Tuesday": "📘",
        "Wednesday": "📖",
        "Thursday": "📝",
        "Friday": "📚",
        "Saturday": "🎉",
        "Sunday": "☕",
    }

    return render(request, "timetable.html", {
        "current_day": current_day,
        "current_icon": day_icons.get(current_day, "📅"),
    })