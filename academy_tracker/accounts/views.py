from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import CustomUserForm, LoginForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings 
from django.http import HttpResponse 
from django.contrib.auth import get_user_model 
from .forms import PendingUserForm 
from .models import PendingUser 

# def register_user(request):
    # if request.method == "POST":
        # form = CustomUserForm(request.POST)
        # if form.is_valid():
            # form.save()
            # return redirect("home")  # redirect after success
    # else:
        # form = CustomUserForm()

    # return render(request, "register.html", {"form": form})

# Register View:
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import PendingUser, CustomUser
from .forms import PendingUserForm

def register_user(request):
    if request.method == "POST":
        form = PendingUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]

            # Check manually before saving
            if PendingUser.objects.filter(email=email).exists():
                form.add_error("email", "A pending account with this email already exists. Please check your email.")
            else:
                pending_user = form.save(commit=False)
                pending_user.save()

                verify_url = request.build_absolute_uri(f"/verify/{pending_user.token}/")

        # if form.is_valid():
        #     pending_user = form.save()

            # verify_url = request.build_absolute_uri(f"/verify/{pending_user.token}/")

            # Send verification email
            # send_mail(
            #     "Verify your StudyMate Account",
            #     f"Hi {pending_user.name},\n\nClick below to verify your account:\n{verify_url}\n\nThis link will expire in 24 hours.\n\nBest,\nStudyMate Team",
            #     settings.DEFAULT_FROM_EMAIL,
            #     [pending_user.email],
            #     fail_silently=False,
            # )
            # Send beautiful HTML verification email
            subject = "Verify your StudyMate Account"
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [pending_user.email]

            context = {
                "name": pending_user.name,
                "verify_url": verify_url,
            }

            html_content = render_to_string("verify_email.html", context)
            text_content = f"Hi {pending_user.name}, please verify your account here: {verify_url}"

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()


            return render(request, "check_email.html", {"email": pending_user.email})
    else:
        form = PendingUserForm()

    return render(request, "register.html", {"form": form})


from django.contrib.auth import login

def verify_email(request, token):
    try:
        pending_user = PendingUser.objects.get(token=token)
    except PendingUser.DoesNotExist:
        return render(request, "email_invalid.html")

    # Check expiration
    if pending_user.is_expired():
        pending_user.delete()
        # return render(request, "email_expired.html")
        return HttpResponse("Invalid Email Error")

    # Create and log in actual verified user
    user = CustomUser.objects.create_user(
        email=pending_user.email,
        name=pending_user.name,
        semester=pending_user.semester,
        password=pending_user.password,  # already hashed in PendingUserForm
    )

    pending_user.delete()

    # ✅ Log in user automatically
    login(request, user)

    # ✅ Redirect to dashboard (change URL name to yours)
    return redirect("student_dashboard")

# Login View :
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



CustomUser = get_user_model()
