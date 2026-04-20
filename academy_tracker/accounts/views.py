from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
#  Explicitly import ALL models used in this file
from academy.models import TimeTable, Task, LearningItem, Subject 
from academy.forms import TimeTableForm, TaskForm, SubjectForm, LearningItemForm
 
from .forms import SignupForm, LoginForm, ProfileEditForm, OTPVerifyForm
from .models import CustomUser, OTPVerification, generate_otp
 
 
# ── helpers ──────────────────────────────────────────────
 
def _send_otp_email(email, otp, name, otp_type='register'):
    """Send styled OTP email using HTML template."""
    subject = "Your StudyMate verification code"
    html_message = render_to_string('otp_email.html', {
        'otp':      otp,
        'name':     name,
        'otp_type': otp_type,
    })
    send_mail(
        subject=subject,
        message=f"Your StudyMate OTP is: {otp}  (expires in 10 minutes)",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html_message,
        fail_silently=False,
    )
 
 
def _create_otp_record(email, otp_type, name='', hashed_password='', semester=1):
    """Invalidate old OTPs and create a fresh one."""
    OTPVerification.objects.filter(
        email=email, otp_type=otp_type, is_used=False
    ).update(is_used=True)   # expire old ones
 
    return OTPVerification.objects.create(
        email=email,
        otp=generate_otp(),
        otp_type=otp_type,
        pending_name=name,
        pending_password=hashed_password,
        pending_semester=semester,
    )
 
 
# ── REGISTER ─────────────────────────────────────────────
 
def register_user(request):
    if request.user.is_authenticated:
        return redirect("student_dashboard")
 
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email    = form.cleaned_data['email']
            name     = form.cleaned_data['name']
            semester = form.cleaned_data['semester']
 
            # Check if email already registered
            if CustomUser.objects.filter(email=email).exists():
                form.add_error('email', 'An account with this email already exists.')
                return render(request, "register.html", {"form": form})
 
            # Build a temp user to get the hashed password — don't save yet
            temp_user = form.save(commit=False)
 
            otp_record = _create_otp_record(
                email=email,
                otp_type='register',
                name=name,
                hashed_password=temp_user.password,
                semester=semester,
            )
 
            try:
                _send_otp_email(email, otp_record.otp, name, 'register')
            except Exception as e:
                print("EMAIL ERROR:", e)
                messages.error(request, f"Failed to send OTP: {e}")
                return render(request, "register.html", {"form": form})
 
            # Store email in session so verify view knows who to verify
            request.session['otp_email']    = email
            request.session['otp_type']     = 'register'
            messages.success(request, f"OTP sent to {email}. Check your inbox.")
            return redirect("verify_otp")
    else:
        form = SignupForm()
 
    return render(request, "register.html", {"form": form})
 
 
# ── LOGIN ─────────────────────────────────────────────────
 
def login_view(request):
    if request.user.is_authenticated:
        return redirect("student_dashboard")
 
    form = LoginForm()
 
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
 
            if user:
                # ── OTP gate: if email not verified yet, send OTP ──
                if not user.is_email_verified:
                    otp_record = _create_otp_record(
                        email=user.email,
                        otp_type='login',
                        name=user.name,
                    )
                    try:
                        _send_otp_email(user.email, otp_record.otp, user.name, 'login')
                    except Exception:
                        form.add_error(None, "Failed to send OTP. Please try again.")
                        return render(request, "login.html", {"form": form})
 
                    request.session['otp_email'] = user.email
                    request.session['otp_type']  = 'login'
                    messages.info(request, f"OTP sent to {user.email}.")
                    return redirect("verify_otp")
 
                # Email already verified → log in directly
                login(request, user)
                return redirect("student_dashboard")
 
            form.add_error(None, "Invalid email or password.")
 
    return render(request, "login.html", {"form": form})
 
 
# ── VERIFY OTP ────────────────────────────────────────────
 
def verify_otp(request):
    email    = request.session.get('otp_email')
    otp_type = request.session.get('otp_type', 'register')
 
    if not email:
        messages.error(request, "Session expired. Please start again.")
        return redirect("register")
 
    form = OTPVerifyForm()
 
    if request.method == "POST":
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
 
            # Fetch the latest unused OTP for this email
            try:
                otp_record = OTPVerification.objects.filter(
                    email=email,
                    otp_type=otp_type,
                    is_used=False,
                ).latest('created_at')
            except OTPVerification.DoesNotExist:
                form.add_error('otp', 'No valid OTP found. Please request a new one.')
                return render(request, "verify_otp.html", {
                    "form": form, "email": email, "otp_type": otp_type
                })
 
            if otp_record.is_expired():
                form.add_error('otp', 'OTP has expired. Please request a new one.')
                return render(request, "verify_otp.html", {
                    "form": form, "email": email, "otp_type": otp_type
                })
 
            if otp_record.otp != entered_otp:
                form.add_error('otp', 'Incorrect OTP. Please try again.')
                return render(request, "verify_otp.html", {
                    "form": form, "email": email, "otp_type": otp_type
                })
 
            # ── OTP is correct ────────────────────────────
            otp_record.is_used = True
            otp_record.save()
 
            if otp_type == 'register':
                # Create the actual user now
                user = CustomUser(
                    email=otp_record.email,
                    name=otp_record.pending_name,
                    semester=otp_record.pending_semester,
                    is_email_verified=True,
                )
                user.password = otp_record.pending_password  # already hashed
                user.save()
                login(request, user)
                del request.session['otp_email']
                del request.session['otp_type']
                messages.success(request, "Email verified! Welcome to StudyMate 🎉")
                return redirect("student_dashboard")
 
            elif otp_type == 'login':
                user = CustomUser.objects.get(email=email)
                user.is_email_verified = True
                user.save()
                login(request, user)
                del request.session['otp_email']
                del request.session['otp_type']
                messages.success(request, "Verified! Welcome back.")
                return redirect("student_dashboard")
 
    return render(request, "verify_otp.html", {
        "form": form, "email": email, "otp_type": otp_type
    })
 
 
# ── RESEND OTP ────────────────────────────────────────────
 
def resend_otp(request):
    email    = request.session.get('otp_email')
    otp_type = request.session.get('otp_type', 'register')
 
    if not email:
        messages.error(request, "Session expired. Please start again.")
        return redirect("register")
 
    # Get name for the email template
    try:
        name = CustomUser.objects.get(email=email).name
    except CustomUser.DoesNotExist:
        # Pending registration — get from last OTP record
        last = OTPVerification.objects.filter(email=email).order_by('-created_at').first()
        name = last.pending_name if last else "Student"
 
    otp_record = _create_otp_record(email=email, otp_type=otp_type, name=name)
 
    try:
        _send_otp_email(email, otp_record.otp, name, otp_type)
        messages.success(request, f"New OTP sent to {email}.")
    except Exception:
        messages.error(request, "Failed to resend OTP. Please try again.")
 
    return redirect("verify_otp")
 
 
# ── LOGOUT ────────────────────────────────────────────────
 
def logout_view(request):
    logout(request)
    return redirect("home")
 
 
# ── HOME ──────────────────────────────────────────────────
 
def home(request):
    return render(request, "home.html")
 

# from academy.views import 
# # 🔥 PROFILE VIEW
# @login_required
# def profile(request):
#     # subject_count = Subject.objects.filter(user=user)
#     total_tasks = Task.objects.filter(user=request.user).count() or 0
#     notes_count = LearningItem.objects.filter(user=request.user).count()  or 0
#     # Subjects ka queryset
#     subjects = (   # ← naam badal diya subjects_count se
#         Subject.objects
#         .filter(semester=request.user.semester)
#         .annotate(
#             total_tasks=Count("task", distinct=True),
#             pending_tasks=Count("task", filter=Q(task__status="Pending")),
#             completed_tasks=Count("task", filter=Q(task__status="Completed")),
#             learning_items_count=Count("learning_items", distinct=True),
#         )
#         .order_by("name", "id")
#     )
#     subjects_count = subjects.count()   # ← Yeh sirf number dega

#     return render(request, "profile.html", {"user": request.user, "total_tasks": total_tasks, "learning_items_count": notes_count, "subjects_count": subjects_count})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Q

@login_required
def profile(request):
    user = request.user

    # -------------------------
    # BASIC COUNTS (user only)
    # -------------------------
    total_tasks = Task.objects.filter(user=user).count()
    notes_count = LearningItem.objects.filter(user=user).count()

    # -------------------------
    # SUBJECTS (ONLY USER'S)
    # -------------------------
    subjects = (
        Subject.objects
        .filter(user=user)   # ✅ FIXED
        .annotate(
            total_tasks=Count("task", distinct=True),
            pending_tasks=Count("task", filter=Q(task__status="Pending")),
            completed_tasks=Count("task", filter=Q(task__status="Completed")),
            learning_items_count=Count("learning_items", distinct=True),
        )
        .order_by("name", "id")
    )

    subjects_count = subjects.count()

    # -------------------------
    # CONTEXT
    # -------------------------
    context = {
        "user": user,
        "total_tasks": total_tasks,
        "learning_items_count": notes_count,
        "subjects_count": subjects_count,
    }

    return render(request, "profile.html", context)


# 🔥 EDIT PROFILE
# ── PROFILE  ───────────────────────────────────
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



