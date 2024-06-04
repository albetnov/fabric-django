from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Count, Sum
import json

from ..models import Color, Customer, Material, Order, SpecialType, Worker


def home(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("Dashboard")

    return redirect("Login")


def dashboard(request: HttpRequest) -> HttpResponse:
    orders_over_time = Order.objects.extra(select={'day': 'date( created_at )'}).values(
        'day').annotate(count=Count('id')).order_by('day')

    orders_by_special_type = SpecialType.objects.annotate(
        order_count=Count('order')).values('name', 'order_count')

    colors_in_orders = Color.objects.annotate(
        order_count=Count('order')).values('name', 'order_count').order_by('-order_count')

    materials_qty = Material.objects.aggregate(total_qty=Sum('qty'))

    customers_over_time = Customer.objects.extra(select={'day': 'date( created_at )'}).values(
        'day').annotate(count=Count('id')).order_by('day')

    workers_over_time = Worker.objects.extra(select={'day': 'date( created_at )'}).values(
        'day').annotate(count=Count('id')).order_by('day')

    total_customers = Customer.objects.count()

    total_workers = Worker.objects.count()

    total_orders = Order.objects.count()

    context = {
        'orders_over_time': json.dumps(list(orders_over_time), default=str),
        'orders_by_special_type': json.dumps(list(orders_by_special_type)),
        'colors_in_orders': json.dumps(list(colors_in_orders)),
        'materials_qty': materials_qty,
        'customers_over_time': json.dumps(list(customers_over_time), default=str),
        'workers_over_time': json.dumps(list(workers_over_time), default=str),
        'total_customers': total_customers,
        'total_workers': total_workers,
        'total_orders': total_orders
    }

    return render(request, "app/dashboard.html", context)
