# make a color crud

from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.db import IntegrityError

from ..models import Color
from ..forms import ColorForm


def index(request: HttpRequest) -> HttpResponse:
    colors = Color.objects.all()

    return render(request, "app/colors/index.html", {"colors": colors})


def create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ColorForm(request.POST)

        if form.is_valid():
            color = Color(
                name=form.cleaned_data["name"],
                hex=form.cleaned_data["hex"],
            )

            try:
                color.save()

                messages.add_message(request, messages.SUCCESS, "Color saved")
                return redirect("Colors")
            except IntegrityError:
                form.add_error("name", "Color already exists")
                return render(request, "app/colors/form.html", {"state": "Create", "form": form})
    else:
        form = ColorForm()

    return render(
        request, "app/colors/form.html", {"state": "Create", "form": form}
    )


def edit(request: HttpRequest, id: int) -> HttpResponse:
    try:
        color = Color.objects.get(id=id)
    except Color.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Color not found")
        return redirect("Colors")

    if request.method == "POST":
        form = ColorForm(request.POST)

        if form.is_valid():
            color.name = form.cleaned_data["name"]
            color.hex = form.cleaned_data["hex"]

            try:
                color.save()

                messages.add_message(request, messages.SUCCESS, "Color saved")
                return redirect("Colors")
            except IntegrityError:
                form.add_error("name", "Color already exists")
                return render(request, "app/colors/form.html", {"state": "Edit", "form": form})
    else:
        form = ColorForm(initial={"name": color.name, "hex": color.hex})

    return render(
        request, "app/colors/form.html", {"state": "Edit", "form": form}
    )


def delete(request: HttpRequest, id: int) -> HttpResponse:
    try:
        color = Color.objects.get(id=id)
        color.delete()

        messages.add_message(request, messages.SUCCESS, "Color deleted")
    except Color.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Color not found")

    return redirect("Colors")
