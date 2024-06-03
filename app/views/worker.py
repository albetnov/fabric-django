from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.db import IntegrityError
from django.contrib import messages

from ..models import Worker
from ..forms import WorkerForm


def index(request: HttpRequest) -> HttpResponse:
    workers = Worker.objects.all()

    return render(request, "app/workers/index.html", {"workers": workers})


def create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = WorkerForm(request.POST)

        if form.is_valid():
            worker = Worker(
                name=form.cleaned_data["name"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
            )

            try:
                worker.save()

                messages.add_message(request, messages.SUCCESS, "Worker saved")
                return redirect("Workers")
            except IntegrityError:
                form.add_error("name", "Worker already exists")
                return render(request, "app/workers/form.html", {"state": "Create", "form": form})
    else:
        form = WorkerForm()

    return render(
        request, "app/workers/form.html", {"state": "Create", "form": form}
    )


def edit(request: HttpRequest, id: int) -> HttpResponse:
    try:
        worker = Worker.objects.get(id=id)
    except Worker.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Worker not found")
        return redirect("Workers")

    if request.method == "POST":
        form = WorkerForm(request.POST)

        if form.is_valid():
            worker.name = form.cleaned_data["name"]
            worker.phone = form.cleaned_data["phone"]
            worker.address = form.cleaned_data["address"]

            try:
                worker.save()

                messages.add_message(request, messages.SUCCESS, "Worker saved")
                return redirect("Workers")
            except IntegrityError:
                form.add_error("name", "Worker already exists")
                return render(request, "app/workers/form.html", {"state": "Edit", "form": form})

    form = WorkerForm(initial={
        "name": worker.name,
        "phone": worker.phone,
        "address": worker.address,
    })

    return render(
        request, "app/workers/form.html", {"state": "Edit", "form": form}
    )


def delete(request: HttpRequest, id: int) -> HttpResponse:
    try:
        worker = Worker.objects.get(id=id)
        worker.delete()
    except Worker.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Worker not found")

    return redirect("Workers")
