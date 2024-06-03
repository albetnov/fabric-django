from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ..models import SpecialType
from ..forms import SpecialTypeForm


def index(request: HttpRequest) -> HttpResponse:
    special_types = SpecialType.objects.all()

    return render(request, "app/special_types/index.html", {"special_types": special_types})


def create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SpecialTypeForm(request.POST)

        if form.is_valid():
            special_type = SpecialType(
                name=form.cleaned_data["name"],
                cloth_type_id=form.cleaned_data["cloth_type"],
            )

            try:
                special_type.save()

                messages.add_message(request, messages.SUCCESS,
                                     "Special type saved")
                return redirect("SpecialTypes")
            except IntegrityError:
                form.add_error("name", "Special type already exists")
                return render(request, "app/special_types/form.html", {
                    "state": "Create", "form": form}
                )
    else:
        form = SpecialTypeForm()

    return render(
        request, "app/special_types/form.html", {
            "state": "Create", "form": form}
    )


def edit(request: HttpRequest, id: int) -> HttpResponse:
    try:
        special_type = SpecialType.objects.get(id=id)
    except SpecialType.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Special type not found")
        return redirect("SpecialTypes")

    if request.method == "POST":
        form = SpecialTypeForm(request.POST)

        if form.is_valid():
            special_type.name = form.cleaned_data["name"]
            special_type.cloth_type_id = form.cleaned_data["cloth_type"]

            try:
                special_type.save()

                messages.add_message(request, messages.SUCCESS,
                                     "Special type updated")
                return redirect("SpecialTypes")
            except IntegrityError:
                form.add_error("name", "Special type already exists")
                return render(request, "app/special_types/form.html", {"state": "Edit", "form": form})
    else:
        form = SpecialTypeForm(
            initial={
                "name": special_type.name,
            }
        )

    return render(
        request, "app/special_types/form.html", {"state": "Edit", "form": form}
    )


def delete(request: HttpRequest, id: int) -> HttpResponse:
    try:
        special_type = SpecialType.objects.get(id=id)
    except SpecialType.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Special type not found")
        return redirect("SpecialTypes")

    special_type.delete()

    messages.add_message(request, messages.SUCCESS, "Special type deleted")
    return redirect("SpecialTypes")
