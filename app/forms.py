from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Submit, Div
from crispy_bootstrap5.bootstrap5 import FloatingField, Field

from .models import Customer, ClothType, Material, Color, Order, SpecialType


class LoginForm(forms.Form):
    staff_id = forms.CharField(label="Staff ID", max_length=50, required=True)
    password = forms.CharField(
        label="Password", required=True, widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper: FormHelper = FormHelper(self)
        self.helper.layout = Layout(
            FloatingField("staff_id", wrapper_class="form-group mb-4"),
            FloatingField("password", wrapper_class="form-group mb-4"),
            Div(
                Submit("submit", "Sign In", css_class="btn-gray-800"),
                css_class="d-grid",
            ),
        )


class CustomerForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200, required=True)
    phone = forms.CharField(
        label="Phone", max_length=50, required=True, widget=forms.NumberInput
    )
    address = forms.CharField(
        label="Address", max_length=1000, required=True, widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper: FormHelper = FormHelper(self)
        self.helper.form_id = "form"
        self.helper.layout = Layout(
            Row(
                Field("name", wrapper_class="form-group mb-4 col-md-6"),
                Field("phone", wrapper_class="form-group mb-4 col-md-6"),
            ),
            Field("address", wrapper_class="form-group mb-4"),
        )


class SpecialTypeForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200, required=True)
    cloth_type = forms.ChoiceField(label="Cloth Type", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper: FormHelper = FormHelper(self)
        self.helper.form_id = "form"
        self.helper.layout = Layout(
            Field("name", wrapper_class="form-group mb-4"),
            Field("cloth_type", wrapper_class="form-group mb-4"),
        )

        self.fields["cloth_type"].choices = [
            (cloth_type.id, cloth_type.name) for cloth_type in ClothType.objects.all()]


class ClothTypeForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper: FormHelper = FormHelper(self)
        self.helper.form_id = "form"
        self.helper.layout = Layout(
            Field("name", wrapper_class="form-group mb-4"),
        )


class MaterialForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200, required=True)
    qty = forms.IntegerField(label="Quantity", required=True)
    price = forms.IntegerField(label="Price", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper: FormHelper = FormHelper(self)
        self.helper.form_id = "form"
        self.helper.layout = Layout(
            Field("name", wrapper_class="form-group mb-4"),
            Row(
                Field("qty", wrapper_class="form-group mb-4 col-md-6"),
                Field("price", wrapper_class="form-group mb-4 col-md-6"),
            ),
        )


class ColorForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200, required=True)
    hex = forms.CharField(label="Hex", max_length=7, required=True,
                          widget=forms.TextInput(attrs={"type": "color"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper: FormHelper = FormHelper(self)
        self.helper.form_id = "form"
        self.helper.layout = Layout(
            Field("name", wrapper_class="form-group mb-4"),
            Field("hex", wrapper_class="form-group mb-4 color-input"),
        )


class WorkerForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200, required=True)
    phone = forms.CharField(
        label="Phone", max_length=50, required=True, widget=forms.NumberInput
    )
    address = forms.CharField(
        label="Address", max_length=1000, required=True, widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper: FormHelper = FormHelper(self)
        self.helper.form_id = "form"
        self.helper.layout = Layout(
            Row(
                Field("name", wrapper_class="form-group mb-4 col-md-6"),
                Field("phone", wrapper_class="form-group mb-4 col-md-6"),
            ),
            Field("address", wrapper_class="form-group mb-4"),
        )


class OrderForm(forms.Form):
    customer = forms.ChoiceField(
        label="Customer",
        required=True,
    )
    special_type = forms.ChoiceField(
        label="Special Type",
        required=True,
    )
    material = forms.ChoiceField(
        label="Material",
        required=True,
    )
    color = forms.ChoiceField(
        label="Color",
        required=True,
    )
    qty = forms.IntegerField(label="Quantity", required=True)
    worker_amount = forms.ChoiceField(label="Worker Amount", required=True, choices=[
        ("little", "Little"),
        ("normal", "Normal"),
        ("many", "Many"),
    ])
    price = forms.IntegerField(label="Price", required=True)
    difficulty = forms.ChoiceField(label="Difficulty", required=True, choices=[
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ])
    size = forms.ChoiceField(label="Size", required=True, choices=[
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("Standard", "Standard"),
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper: FormHelper = FormHelper(self)
        self.helper.form_id = "form"
        self.helper.layout = Layout(
            Row(
                Field("customer", wrapper_class="form-group mb-4 col-md-6"),
                Field("special_type", wrapper_class="form-group mb-4 col-md-6"),
            ),
            Row(
                Field("material", wrapper_class="form-group mb-4 col-md-6"),
                Field("color", wrapper_class="form-group mb-4 col-md-6"),
            ),
            Row(
                Field("qty", wrapper_class="form-group mb-4 col-md-4"),
                Field("worker_amount", wrapper_class="form-group mb-4 col-md-4"),
                Field("price", wrapper_class="form-group mb-4 col-md-4"),
            ),
            Row(
                Field("size", wrapper_class="form-group mb-4 col-md-4"),
                Field("difficulty", wrapper_class="form-group mb-4 col-md-4"),
            )
        )

        self.fields["customer"].choices = [
            (customer.id, customer.name) for customer in Customer.objects.all()
        ]
        self.fields["special_type"].choices = [
            (special_type.id, special_type.name +
             " - " + special_type.cloth_type.name)
            for special_type in SpecialType.objects.all()
        ]
        self.fields["material"].choices = [
            (material.id, material.name)
            for material in Material.objects.all()
        ]
        self.fields["color"].choices = [
            (color.id, color.name) for color in Color.objects.all()
        ]


class PredictForm(forms.Form):
    order = forms.ChoiceField(
        label="Order",
        required=True,
    )

    model_type = forms.ChoiceField(
        label="Model Type",
        required=True,
        choices=[
            ("rf", "Model RF"),
            ("dt", "Model DT")
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper: FormHelper = FormHelper(self)
        self.helper.form_id = "form"
        self.helper.layout = Layout(
            Row(
                Field("order", wrapper_class="form-group mb-4 col-md-6"),
                # Field("model_type", wrapper_class="form-group mb-4 col-md-6"),
            ),
        )

        format = "%Y-%m-%d"

        self.fields["order"].choices = [(0, 'Select Order')] + [
            (order.id, f"{order.ref_id} - {order.customer.name} - {order.created_at.strftime(format)}") for order in Order.objects.all()
        ]


class UserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=200, required=True)
    password = forms.CharField(
        label="Password", required=True, widget=forms.PasswordInput
    )
    first_name = forms.CharField(label="First Name", max_length=200)
    last_name = forms.CharField(label="Last Name", max_length=200)
    is_active = forms.BooleanField(label="Active", required=False)
    email = forms.EmailField(label="Email", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper: FormHelper = FormHelper(self)
        self.helper.form_id = "form"
        self.helper.layout = Layout(
            Row(
                Field("email", wrapper_class="form-group mb-4 col-md-6"),
                Field("username", wrapper_class="form-group mb-4 col-md-6"),
            ),
            Row(
                Field("first_name", wrapper_class="form-group mb-4 col-md-6"),
                Field("last_name", wrapper_class="form-group mb-4 col-md-6"),
            ),
            Field("password", wrapper_class="form-group mb-4"),
            Field("is_active", wrapper_class="form-group mb-4"),
        )
