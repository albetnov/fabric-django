from time import time
from django.core.management.base import BaseCommand
import pandas as pd
import pathlib

from .utils import Seeder


class Command(BaseCommand):
    help = "Seed the database with fake data (Also resets it!)"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=None)

    def handle(self, *args, **options):
        startTime = time()
        csvPath = pathlib.Path(
            __file__).parent.absolute().joinpath("data_baju.csv")

        limit = options["limit"]

        df = pd.read_csv(csvPath)
        seeder = Seeder(df)

        seeder.handle_types(limit=limit)
        seeder.handle_colors(limit=limit)
        seeder.handle_materials(limit=limit)
        seeder.handle_workers(limit=50 if limit is None else limit)
        seeder.handle_customer(limit=50 if limit is None else limit)
        seeder.handle_orders(limit=limit)

        endTime = time()

        print(f"Seeding completed in {endTime - startTime}")
