from time import time
from django.core.management.base import BaseCommand
from django.db import IntegrityError
import pandas as pd
import pathlib

from ulid import ULID
from faker import Faker

from app.models import ClothType, Color, Customer, Material, SpecialType, Worker, Order


class Command(BaseCommand):
    help = "Seed the database with fake data (Also resets it!)"

    def handle_types(self, df: pd.DataFrame):
        ClothType.objects.all().delete()

        for cloth_type in df["Jenis"].unique():
            clothType = ClothType.objects.create(name=cloth_type)

            for specials in df.loc[df["Jenis"] == cloth_type, "Khusus"].unique():
                try:
                    SpecialType.objects.create(
                        name=specials, cloth_type_id=clothType.id)
                except IntegrityError:
                    pass

    def handle_colors(self, df: pd.DataFrame):
        Color.objects.all().delete()

        for color in df["color"].unique():
            Color.objects.create(name=color, hex="#000000")

    def handle_materials(self, df: pd.DataFrame):
        Material.objects.all().delete()

        for material in df["Bahan"].unique():
            Material.objects.create(name=material, qty=99, price=10000)

    def handle_workers(self):
        fake = Faker()
        for _ in range(300):
            Worker.objects.create(
                name=fake.name(), phone=fake.phone_number(), address=fake.address())

    def handle_customer(self):
        fake = Faker()
        for _ in range(300):
            Customer.objects.create(
                name=fake.name(), phone=fake.phone_number(), address=fake.address())

    def transWorkerAmount(self, amount: str) -> str:
        if amount == "Sedikit":
            return "little"
        elif amount == "Banyak":
            return "many"
        else:
            return "normal"

    def transComplexity(self, complexity: str) -> str:
        if complexity == "Rendah":
            return "easy"
        elif complexity == "Tinggi":
            return "hard"
        else:
            return "medium"

    def handle_orders(self, df: pd.DataFrame):
        fake = Faker()
        for _, row in df.iterrows():
            special_type = SpecialType.objects.get(name=row["Khusus"])
            material = Material.objects.get(name=row["Bahan"])
            color = Color.objects.get(name=row["color"])
            random_customer = Customer.objects.order_by("?").first()

            Order.objects.create(
                ref_id=str(ULID()),
                customer_id=random_customer.id,
                special_type_id=special_type.id,
                material_id=material.id,
                color_id=color.id,
                qty=row["Order Quantity"],
                worker_amount=self.transWorkerAmount(
                    row["Jumlah Pekerja"] if row["Jumlah Pekerja"] != "Bedikit" else "Sedikit"),
                price=fake.random_int(min=50_000, max=1_000_000),
                complexity=self.transComplexity(row["Kompleksitas"]),
                size="Standard" if row["Size"] == "Standar" else row["Size"]
            )

    def handle(self, *args, **options):
        startTime = time()
        csvPath = pathlib.Path(
            __file__).parent.absolute().joinpath("data_baju.csv")

        df = pd.read_csv(csvPath)

        self.handle_types(df)
        self.handle_colors(df)
        self.handle_materials(df)
        self.handle_workers()
        self.handle_customer()
        self.handle_orders(df)

        endTime = time()

        print(f"Seeding completed in {endTime - startTime}")
