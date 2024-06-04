from django.contrib import admin

from .models import Customer, ClothType, SpecialType, Material, Color, Worker, Order

admin.site.register(Customer)
admin.site.register(ClothType)
admin.site.register(SpecialType)
admin.site.register(Material)
admin.site.register(Color)
admin.site.register(Worker)
admin.site.register(Order)
