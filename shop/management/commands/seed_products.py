from decimal import Decimal
import random

from django.core.management.base import BaseCommand

from shop.models import Category, Product


class Command(BaseCommand):
    help = "Seed the database with dummy categories and 10 products for testing."

    def handle(self, *args, **options):
        category_names = ["Electronics", "Books", "Clothing"]

        categories = []
        for name in category_names:
            category, _ = Category.objects.get_or_create(
                name=name,
                defaults={"slug": name.lower().replace(" ", "-")},
            )
            categories.append(category)

        created_count = 0
        for i in range(1, 11):
            category = random.choice(categories)
            name = f"Sample Product {i}"
            slug = f"sample-product-{i}"

            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "slug": slug,
                    "description": "This is a dummy product used for development and testing.",
                    "price": Decimal(random.randrange(1000, 10000)) / 100,
                    "stock": random.randint(1, 50),
                    "available": True,
                },
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Seeded {created_count} product(s) successfully.")
        )

