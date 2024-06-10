from django.core.management.base import BaseCommand
import pandas as pd
import pathlib
from ui.settings import USE_POSTGRES

from .utils import Seeder, handle_sqlite, handle_postgres


class Command(BaseCommand):
    supported_modules = ["types", "colors",
                         "materials", "workers", "customers", "orders"]

    # take an argument module to restore
    def add_arguments(self, parser):
        parser.add_argument("module", type=str)

        # also take an optional parameter --delete to delete the entire module
        parser.add_argument("--no-delete", action="store_true")

        # also take an optional parameter --count to specify the number of entry to restore
        parser.add_argument("--count", type=int, default=0)

        parser.add_argument("--restore-related", action="store_true")

    def query_db_by_tables(self, tables):
        if not USE_POSTGRES:
            handle_sqlite(tables)
            return

        handle_postgres(tables)

    def handle(self, *args, **options):
        # get the module name
        module = options["module"]
        no_delete = options["no_delete"]
        count = options["count"]
        restore_related = options["restore_related"]

        depend_on_orders = ["types", "materials", "colors"]

        if module not in self.supported_modules:
            print(f"Module {module} is not supported")
            print(f"Supported modules: {', '.join(self.supported_modules)}")
            return

        if not no_delete:
            print(
                f"Warning: this might remove other existing data that related to {module}.")

            # ask for confirmation input
            confirm = input("Are you sure you want to continue? (y/n): ")
            if confirm.lower() != "y":
                print("Aborting...")
                return

            if module in depend_on_orders:
                print(f"Deleting related tables to {module} (app_order)")

                confirm = input(
                    "Are you sure you want to continue? (y/n): ")
                if confirm.lower() != "y":
                    print("Aborting...")
                    return

                print("Deleting related tables...")
                self.query_db_by_tables(["app_order"])

        csvPath = pathlib.Path(
            __file__).parent.absolute().joinpath("data_baju.csv")
        df = pd.read_csv(csvPath)

        seeder = Seeder(df)

        seeder_per_module = {
            "types": seeder.handle_types,
            "colors": seeder.handle_colors,
            "materials": seeder.handle_materials,
            "workers": seeder.handle_workers,
            "customers": seeder.handle_customer,
            "orders": seeder.handle_orders
        }

        if not no_delete:
            tables_per_module = {
                "types": ["app_clothtype", "app_specialtype"],
                "colors": ["app_color"],
                "materials": ["app_material"],
                "workers": ["app_worker"],
                "customers": ["app_customer"],
                "orders": ["app_order"]
            }
            self.query_db_by_tables(tables_per_module[module])

        seeder_per_module[module](limit=count if count > 0 else None)

        if restore_related and module in depend_on_orders:
            seeder.handle_orders(limit=count if count > 0 else None)
            print("Orders restored")
