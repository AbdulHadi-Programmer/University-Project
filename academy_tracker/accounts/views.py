from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import CustomUserForm, LoginForm, ProfileEditForm
from django.contrib.auth.decorators import login_required

def register_user(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")  # redirect after success
    else:
        form = CustomUserForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("student_dashboard")  # replace with your homepage
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")  # back to login page


@login_required
def edit_profile(request):
    user = request.user 

    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")  # redirect to profile page after editing
    else: 
        form = ProfileEditForm(instance=user)
    return render(request, "edit_profile.html", {"form": form})

@login_required
def profile(request):
    return render(request, "profile.html", {"user": request.user})

def home(request):
    return render(request, "home.html")  # create templates/home.html

# def timetable(request):
    # return render(request, "timetable.html")

from datetime import datetime

# def timetable(request):
#     # Get current day name (e.g., Monday, Tuesday)
#     current_day = datetime.now().strftime('%A')

#     # Map each day to an emoji/icon
#     day_icons = {
#         "Monday": "🌞",
#         "Tuesday": "📘",
#         "Wednesday": "📖",
#         "Thursday": "📝",
#         "Friday": "📚",
#         "Saturday": "🎉",
#         "Sunday": "☕",
#     }

#     # Pick correct icon
#     current_icon = day_icons.get(current_day, "📅")

#     return render(request, "timetable.html", {
#         "current_day": current_day,
#         "current_icon": current_icon,
#     })


from datetime import datetime

def timetable (request):
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
    current_icon = day_icons.get(current_day, "📅")

    return render(request, "timetable.html", {
        "current_day": current_day,
        "current_icon": current_icon,
    })
