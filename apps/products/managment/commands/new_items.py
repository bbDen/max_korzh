from django.core.management.base import BaseCommand, CommandError

from datetime import datetime, timedelta

from apps.products.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        Product.objects.filter(created_at__lte=datetime.now()-timedelta(days=2)).update(new=False)
        self.stdout.write('Updated product older than 2 days')
