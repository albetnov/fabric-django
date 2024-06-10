from django.db import connection, IntegrityError
from ulid import ULID
from faker import Faker

from app.models import ClothType, Color, Customer, Material, SpecialType, Worker, Order


def sqlite_delete_table(table: str):
    with connection.cursor() as cursor:
        print(f"Deleting {table}")
        cursor.execute(f"DELETE FROM {table}")
        cursor.execute(
            f"DELETE FROM SQLITE_SEQUENCE WHERE name = '{table}'")


def handle_sqlite(tables):
    for table in tables:
        sqlite_delete_table(table)


def handle_postgres(tables):
    with connection.cursor() as cursor:
        for table in tables:
            print(table)
            cursor.execute(f"TRUNCATE TABLE {
                           table} RESTART IDENTITY CASCADE")


class Seeder:
    def __init__(self, df):
        self.df = df

    def handle_types(self, limit):
        ClothType.objects.all().delete()

        for cloth_type in self.df["Jenis"].unique() if limit is None else self.df["Jenis"].unique()[:limit]:
            clothType = ClothType.objects.create(name=cloth_type)

            for specials in self.df.loc[self.df["Jenis"] == cloth_type, "Khusus"].unique():
                try:
                    SpecialType.objects.create(
                        name=specials, cloth_type_id=clothType.id)
                except IntegrityError:
                    pass

    def handle_colors(self, limit):
        Color.objects.all().delete()

        for color in self.df["color"].unique() if limit is None else self.df["color"].unique()[:limit]:
            Color.objects.create(name=color, hex="#000000")

    def handle_materials(self, limit):
        Material.objects.all().delete()

        for material in self.df["Bahan"].unique() if limit is None else self.df["Bahan"].unique()[:limit]:
            Material.objects.create(name=material, qty=99, price=10000)

    def handle_workers(self, limit=50):
        fake = Faker()
        for _ in range(limit if not None else 50):
            Worker.objects.create(
                name=fake.name(), phone=fake.phone_number(), address=fake.address())

    def handle_customer(self, limit=50):
        fake = Faker()
        for _ in range(limit if not None else 50):
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

    def handle_orders(self, limit):
        fake = Faker()
        count = 0
        for _, row in self.df.iterrows():
            if count == limit:
                break

            count += 1
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
