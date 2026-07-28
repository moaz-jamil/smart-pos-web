from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.forms import LoginForm, RegisterBusinessForm, UserProfileForm
from authentication.models import User, Business
from settings_app.models import BusinessSetting
from branches.models import Branch

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


def register_business_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterBusinessForm(request.POST)
        if form.is_valid():
            business = form.save()
            # Create Default Business Settings & Default Branch
            BusinessSetting.objects.create(business=business)
            branch = Branch.objects.create(business=business, name="Main Store", code="BR-001")

            # Create Business Owner User
            owner = User.objects.create_user(
                username=form.cleaned_data['owner_username'],
                email=form.cleaned_data['owner_email'],
                password=form.cleaned_data['owner_password'],
                role=User.ROLE_ADMIN,
                business=business,
                branch=branch,
                is_staff=True
            )
            branch.manager = owner
            branch.save()

            login(request, owner)
            messages.success(request, "Business registered successfully!")
            return redirect('dashboard')
    else:
        form = RegisterBusinessForm()

    return render(request, 'authentication/register.html', {'form': form})


@login_required
def user_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'authentication/profile.html', {'form': form})
