from django.urls import path

from .views import customer, home, auth, cloth_type, special_type, material, color, worker, predict, order, user

urlpatterns = [
    path("", home.home, name="Home"),

    path("login", auth.login, name="Login"),
    path("logout", auth.logout, name="Logout"),

    path("dashboard", home.dashboard, name="Dashboard"),

    path("customers", customer.index, name="Customers"),
    path("customers/create", customer.create, name="CustomerCreate"),
    path("customers/edit/<int:id>", customer.edit, name="CustomerEdit"),
    path("customers/delete/<int:id>",
         customer.delete, name="CustomerDelete"),

    path("special-types", special_type.index, name="SpecialTypes"),
    path("special-types/create", special_type.create,
         name="SpecialTypeCreate"),
    path("special-types/edit/<int:id>",
         special_type.edit, name="SpecialTypeEdit"),
    path("special-types/delete/<int:id>",
         special_type.delete, name="SpecialTypeDelete"),

    path("cloth-types", cloth_type.index, name="ClothTypes"),
    path("cloth-types/create", cloth_type.create, name="ClothTypeCreate"),
    path("cloth-types/edit/<int:id>", cloth_type.edit, name="ClothTypeEdit"),
    path("cloth-types/delete/<int:id>",
         cloth_type.delete, name="ClothTypeDelete"),

    path("materials", material.index, name="Materials"),
    path("materials/create", material.create, name="MaterialCreate"),
    path("materials/edit/<int:id>", material.edit, name="MaterialEdit"),
    path("materials/delete/<int:id>", material.delete, name="MaterialDelete"),

    path("colors", color.index, name="Colors"),
    path("colors/create", color.create, name="ColorCreate"),
    path("colors/edit/<int:id>", color.edit, name="ColorEdit"),
    path("colors/delete/<int:id>", color.delete, name="ColorDelete"),

    path("workers", worker.index, name="Workers"),
    path("workers/create", worker.create, name="WorkerCreate"),
    path("workers/edit/<int:id>", worker.edit, name="WorkerEdit"),
    path("workers/delete/<int:id>", worker.delete, name="WorkerDelete"),

    path("orders", order.index, name="Orders"),
    path("orders/create", order.create, name="OrderCreate"),
    path("orders/delete/<int:id>", order.delete, name="OrderDelete"),
    path("orders/show/<int:id>", order.show, name="OrderShow"),

    path("predict", predict.index, name="Predict"),
    path("predict/get/order", predict.order, name="PredictGetOrder"),

    path("users", user.index, name="Users"),
    path("users/create", user.create, name="UserCreate"),
    path("users/edit/<int:id>", user.edit, name="UserEdit"),
    path("users/delete/<int:id>", user.delete, name="UserDelete"),
]
