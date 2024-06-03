from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from ..forms import UserForm


def index(request: HttpRequest) -> HttpResponse:
    users = User.objects.all()

    return render(request, "app/users/index.html", {"users": users})


def create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                is_active=form.cleaned_data["is_active"],
            )

            messages.add_message(request, messages.SUCCESS, "User saved")
            return redirect("Users")
    else:
        form = UserForm()

    return render(request, "app/users/form.html", {"state": "Create", "form": form})


def edit(request: HttpRequest, id: int) -> HttpResponse:
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        messages.add_message(request, messages.ERROR, "User not found")
        return redirect("Users")

    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            user.username = form.cleaned_data["username"]
            user.email = form.cleaned_data["email"]
            user.password = form.cleaned_data["password"]
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.is_active = form.cleaned_data["is_active"]
            user.save()

            messages.add_message(request, messages.SUCCESS, "User updated")
            return redirect("Users")
    else:
        form = UserForm(
            initial={
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
            }
        )

    return render(request, "app/users/form.html", {"state": "Edit", "form": form})


def delete(request: HttpRequest, id: int) -> HttpResponse:
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        messages.add_message(request, messages.ERROR, "User not found")
        return redirect("Users")

    user.delete()

    messages.add_message(request, messages.SUCCESS, "User deleted")
    return redirect("Users")
