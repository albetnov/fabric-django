from django.core.management.base import BaseCommand
from ui.settings import USE_POSTGRES

from . import utils


class Command(BaseCommand):
    help = "Reset the database"
    tables = ["app_order", "app_worker", "app_color", "app_material",
              "app_specialtype", "app_clothtype", "app_customer"]

    def handle(self, *args, **options):
        if not USE_POSTGRES:
            utils.handle_sqlite(self.tables)
            print("Database reset complete")
            return

        utils.handle_postgres(self.tables)
        print("Database reset complete")
        return
