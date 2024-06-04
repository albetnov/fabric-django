from django.core.management.base import BaseCommand
from django.db import connection
from ui.settings import USE_POSTGRES


class Command(BaseCommand):
    help = "Reset the database"
    tables = ["app_order", "app_worker", "app_color", "app_material",
              "app_specialtype", "app_clothtype", "app_customer"]

    def sqlite_delete_table(self, table: str):
        with connection.cursor() as cursor:
            print(f"Deleting {table}")
            cursor.execute(f"DELETE FROM {table}")
            cursor.execute(
                f"DELETE FROM SQLITE_SEQUENCE WHERE name = '{table}'")

    def handle_sqlite(self):
        for table in self.tables:
            self.sqlite_delete_table(table)

    def handle_postgres(self):
        with connection.cursor() as cursor:
            for table in self.tables:
                print(table)
                cursor.execute(f"TRUNCATE TABLE {
                               table} RESTART IDENTITY CASCADE")

    def handle(self, *args, **options):
        if not USE_POSTGRES:
            self.handle_sqlite()
            print("Database reset complete")
            return

        self.handle_postgres()
        print("Database reset complete")
        return
