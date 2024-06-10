import pathlib
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.http.response import json
from django.shortcuts import render
import joblib
import pandas as pd
from datetime import timedelta
import pytz

from ..forms import PredictForm
from ..models import Order


def transWorkerAmount(amount: str) -> str:
    if amount == "little":
        return "Sedikit"
    elif amount == "many":
        return "Banyak"
    else:
        return "Sedang"


def transComplexity(complexity: str) -> str:
    if complexity == "easy":
        return "Rendah"
    elif complexity == "hard":
        return "Tinggi"
    else:
        return "Menengah"


def index(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PredictForm(request.POST)
        if form.is_valid():
            order = Order.objects.get(id=form.cleaned_data["order"])

            if order is None:
                return HttpResponseNotFound(json.dumps({"result": "Order not found"}))

            input = {
                "Order Quantity": order.qty,
                "Jenis": order.special_type.cloth_type.name,
                "Khusus": order.special_type.name,
                "Size": order.size,
                "Kompleksitas": transComplexity(order.complexity),
                "Bahan": order.material.name,
                "color": order.color.name,
                "Jumlah Pekerja": transWorkerAmount(order.worker_amount)
            }

            input_df = pd.DataFrame([input])
            model_type = form.cleaned_data["model_type"]

            model_path = pathlib.Path(__file__).parent.parent.absolute().joinpath(
                "models").joinpath("production_time.pkl" if model_type == "rf" else "production_time_decisionTree.pkl")

            model = joblib.load(model_path)

            result = model.predict(input_df)[0]

            current_date = pd.Timestamp.now().to_pydatetime().replace(
                tzinfo=pytz.timezone("Asia/Jakarta"))

            order_created_at_aware = order.created_at.astimezone(pytz.timezone("Asia/Jakarta")).replace(
                second=0, microsecond=0)
            current_date = current_date.replace(second=0, microsecond=0)
            estimation_date = order_created_at_aware + timedelta(hours=result)

            return HttpResponse(json.dumps({
                "date": estimation_date.strftime("%Y-%m-%d"),
                "time": estimation_date.strftime("%H:%M"),
                "result": result,
                "order_date": order_created_at_aware.strftime("%Y-%m-%d %H:%M"),
                "done": current_date >= estimation_date
            }))
    else:
        form = PredictForm()

    return render(request, "app/predicts/index.html", {"form": form})


def order(request: HttpRequest) -> HttpResponse:
    orderId = request.GET.get("order")

    order = Order.objects.get(id=orderId)

    if order is not None:
        return HttpResponse(json.dumps({"result": {
            "customer": order.customer.name,
            "material": order.material.name,
            "qty": order.qty,
            "price": order.price,
            "special_type": order.special_type.name,
            "color": order.color.name,
            "worker_amount": order.worker_amount,
            "difficulty": order.complexity,
            "cloth_type": order.special_type.cloth_type.name,
            "size": order.size,
            "order_id": order.id,
            "order_date": order.created_at.strftime("%Y-%m-%d %H:%M")
        }}))

    return HttpResponseNotFound(json.dumps({"result": "Order not found"}))
