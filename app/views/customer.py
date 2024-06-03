from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ..models import Customer
from ..forms import CustomerForm


def index(request: HttpRequest) -> HttpResponse:
    customers = Customer.objects.all()

    return render(request, "app/customers/index.html", {"customers": customers})


def create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CustomerForm(request.POST)

        if form.is_valid():
            customer = Customer(
                name=form.cleaned_data["name"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
            )
            customer.save()

            messages.add_message(request, messages.SUCCESS, "Customer saved")
            return redirect("Customers")
    else:
        form = CustomerForm()

    return render(
        request, "app/customers/form.html", {"state": "Create", "form": form}
    )


def edit(request: HttpRequest, id: int) -> HttpResponse:
    try:
        customer = Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Customer not found")
        return redirect("Customers")

    if request.method == "POST":
        form = CustomerForm(request.POST)

        if form.is_valid():
            customer.name = form.cleaned_data["name"]
            customer.phone = form.cleaned_data["phone"]
            customer.address = form.cleaned_data["address"]
            customer.save()

            messages.add_message(request, messages.SUCCESS, "Customer updated")
            return redirect("Customers")
    else:
        form = CustomerForm(
            initial={
                "name": customer.name,
                "phone": customer.phone,
                "address": customer.address,
            }
        )

    return render(request, "app/customers/form.html", {"state": "Edit", "form": form})


def delete(request: HttpRequest, id: int) -> HttpResponse:
    try:
        customer = Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Customer not found")
        return redirect("Customers")

    customer.delete()

    messages.add_message(request, messages.SUCCESS, "Customer deleted")
    return redirect("Customers")
