from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ..models import ClothType
from ..forms import ClothTypeForm


def index(request: HttpRequest) -> HttpResponse:
    cloth_types = ClothType.objects.all()

    return render(request, "app/cloth_types/index.html", {"cloth_types": cloth_types})


def create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ClothTypeForm(request.POST)

        if form.is_valid():
            cloth_type = ClothType(
                name=form.cleaned_data["name"],
            )

            try:
                cloth_type.save()

                messages.add_message(
                    request, messages.SUCCESS, "Cloth type saved")
                return redirect("ClothTypes")
            except IntegrityError:
                form.add_error("name", "Cloth type already exists")
                return render(request, "app/cloth_types/form.html", {"state": "Create", "form": form})

    else:
        form = ClothTypeForm()

    return render(
        request, "app/cloth_types/form.html", {"state": "Create", "form": form}
    )


def edit(request: HttpRequest, id: int) -> HttpResponse:
    try:
        cloth_type = ClothType.objects.get(id=id)
    except ClothType.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Cloth type not found")
        return redirect("ClothTypes")

    if request.method == "POST":
        form = ClothTypeForm(request.POST)

        if form.is_valid():
            cloth_type.name = form.cleaned_data["name"]

            try:
                cloth_type.save()

                messages.add_message(request, messages.SUCCESS,
                                     "Cloth type updated")
                return redirect("ClothTypes")
            except IntegrityError:
                form.add_error("name", "Cloth type already exists")
                return render(request, "app/cloth_types/form.html", {"state": "Create", "form": form})
    else:
        form = ClothTypeForm(
            initial={
                "name": cloth_type.name,
            }
        )

    return render(
        request, "app/cloth_types/form.html", {"state": "Edit", "form": form}
    )


def delete(request: HttpRequest, id: int) -> HttpResponse:
    try:
        cloth_type = ClothType.objects.get(id=id)
    except ClothType.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Cloth type not found")
        return redirect("ClothTypes")

    cloth_type.delete()

    messages.add_message(request, messages.SUCCESS, "Cloth type deleted")
    return redirect("ClothTypes")
