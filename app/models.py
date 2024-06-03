from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    address = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)


class ClothType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)


class SpecialType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    cloth_type = models.ForeignKey(ClothType, on_delete=models.CASCADE)


class Material(models.Model):
    name = models.CharField(max_length=200, unique=True)
    qty = models.IntegerField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)


class Color(models.Model):
    name = models.CharField(max_length=200, unique=True)
    hex = models.CharField(max_length=7)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)


class Worker(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    address = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)


class Order(models.Model):
    ref_id = models.CharField(max_length=200, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    special_type = models.ForeignKey(SpecialType, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    qty = models.IntegerField()
    worker_amount = models.CharField(max_length=100)
    price = models.IntegerField()
    complexity = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
