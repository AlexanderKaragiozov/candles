from django.core.management.base import BaseCommand
from django.utils.timezone import now
from candle.models import CandleOrder
from candle.spreadsheet import delete_deadline_orders

class Command(BaseCommand):
    help = "Deletes expired orders from the CandleOrder table"

    def handle(self, *args, **kwargs):
        expired_orders = CandleOrder.objects.filter(deadline__lt=now())
        deleted_count, _ = expired_orders.delete()
        for order in expired_orders:
            delete_deadline_orders(order.id)
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} expired orders."))
