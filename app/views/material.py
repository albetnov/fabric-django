from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ..models import Material
from ..forms import MaterialForm


def index(request: HttpRequest) -> HttpResponse:
    materials = Material.objects.all()

    return render(request, "app/materials/index.html", {"materials": materials})


def create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = MaterialForm(request.POST)

        if form.is_valid():
            material = Material(
                name=form.cleaned_data["name"],
                qty=form.cleaned_data["qty"],
                price=form.cleaned_data["price"],
            )

            try:
                material.save()

                messages.add_message(request, messages.SUCCESS,
                                     "Material saved")
                return redirect("Materials")
            except IntegrityError:
                form.add_error("name", "Material already exists")
                return render(request, "app/materials/form.html", {
                    "state": "Create", "form": form}
                )
    else:
        form = MaterialForm()

    return render(
        request, "app/materials/form.html", {
            "state": "Create", "form": form}
    )


def edit(request: HttpRequest, id: int) -> HttpResponse:
    try:
        material = Material.objects.get(id=id)
    except Material.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Material not found")
        return redirect("Materials")

    if request.method == "POST":
        form = MaterialForm(request.POST)

        if form.is_valid():
            material.name = form.cleaned_data["name"]
            material.qty = form.cleaned_data["qty"]
            material.price = form.cleaned_data["price"]

            try:
                material.save()

                messages.add_message(request, messages.SUCCESS,
                                     "Material updated")
                return redirect("Materials")
            except IntegrityError:
                form.add_error("name", "Material already exists")
                return render(request, "app/materials/form.html", {
                    "state": "Edit", "form": form}
                )

    form = MaterialForm(initial={"name": material.name, "qty": material.qty,
                                 "price": material.price})

    return render(request, "app/materials/form.html", {
        "state": "Edit", "form": form}
    )


def delete(request: HttpRequest, id: int) -> HttpResponse:
    try:
        material = Material.objects.get(id=id)
    except Material.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Material not found")
        return redirect("Materials")

    material.delete()

    messages.add_message(request, messages.SUCCESS, "Material deleted")
    return redirect("Materials")
