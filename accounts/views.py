
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token


@ensure_csrf_cookie
@never_cache
def login_page(request):

    if request.method == "POST":

        action = request.POST.get("action")

        # SIGNUP
        if action == "signup":

            name = request.POST.get("name", "").strip()
            email = request.POST.get("email", "").strip().lower()
            password = request.POST.get("password", "")
            terms = request.POST.get("terms")

            if not name or not email or not password:
                messages.error(request, "Please fill all required fields.")
                return redirect("login")

            if not terms:
                messages.error(request, "Please accept the terms.")
                return redirect("login")

            if len(password) < 8 or not any(char.isdigit() for char in password):
                messages.error(
                    request,
                    "Password must have at least 8 characters and one number."
                )
                return redirect("login")

            if User.objects.filter(email=email).exists():
                messages.error(
                    request,
                    "Email already registered. Please login."
                )
                return redirect("login")

            User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )

            return render(
                request,
                "accounts/login.html",
                {
                    "signup_success": True,
                    "signup_name": name,
                    "signup_email": email,
                }
            )

        # LOGIN
        elif action == "login":

            email = request.POST.get("email", "").strip().lower()
            password = request.POST.get("password", "")

            if not email or not password:
                messages.error(
                    request,
                    "Please enter email and password."
                )
                return redirect("login")

            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user is not None:

                login(request, user)

                # Generate fresh CSRF token after login
                get_token(request)

                # Show original Colorlib success screen
                return render(
                    request,
                    "accounts/login.html",
                    {
                        "login_success": True,
                    }
                )

            messages.error(
                request,
                "Incorrect email or password. Please try again."
            )
            return redirect("login")

    return render(request, "accounts/login.html")


# DASHBOARD
@never_cache
def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "accounts/dashboard.html")
