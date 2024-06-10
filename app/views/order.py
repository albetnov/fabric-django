from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.db import IntegrityError, transaction
from ulid import ULID

from ..models import Order, Material
from ..forms import OrderForm


def index(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.all()

    return render(request, "app/orders/index.html", {"orders": orders})


@transaction.atomic
def create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            order = Order(
                customer_id=form.cleaned_data["customer"],
                material_id=form.cleaned_data["material"],
                qty=form.cleaned_data["qty"],
                price=form.cleaned_data["price"],
                special_type_id=form.cleaned_data["special_type"],
                color_id=form.cleaned_data["color"],
                worker_amount=form.cleaned_data["worker_amount"],
                complexity=form.cleaned_data["difficulty"],
                size=form.cleaned_data["size"],
                ref_id=str(ULID())
            )

            material = Material.objects.filter(
                id=form.cleaned_data["material"]).first()

            if material.qty < form.cleaned_data["qty"]:
                form.add_error("qty", "Not enough material")
                return render(request, "app/orders/form.html", {"state": "Create", "form": form})

            material.qty -= form.cleaned_data["qty"]

            try:
                order.save()
                material.save()

                messages.add_message(request, messages.SUCCESS, "Order saved")
                return redirect("Orders")
            except IntegrityError:
                form.add_error("name", "Order already exists")
                return render(request, "app/orders/form.html", {"state": "Create", "form": form})
    else:
        form = OrderForm()

    return render(
        request, "app/orders/form.html", {"state": "Create", "form": form}
    )


def show(request: HttpRequest, id: int) -> HttpResponse:
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Order not found")
        return redirect("Orders")

    return render(request, "app/orders/show.html", {"order": order})


def delete(request: HttpRequest, id: int) -> HttpResponse:
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Order not found")
        return redirect("Orders")

    order.delete()

    messages.add_message(request, messages.SUCCESS, "Order deleted")
    return redirect("Orders")
