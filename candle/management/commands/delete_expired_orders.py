from django.core.management.base import BaseCommand
from django.utils.timezone import now
from candle.models import CandleOrder
from candle.spreadsheet import delete_deadline_orders

class Command(BaseCommand):
    help = "Deletes expired orders from the CandleOrder table"

    def handle(self, *args, **kwargs):
        expired_orders = CandleOrder.objects.filter(deadline__lt=now(),confirmed=False)

        for order in expired_orders:
            if not order.confirmed:
                order.candle.quantity += order.quantity
                order.candle.save()
                delete_deadline_orders(order.id)
        deleted_count, _ = expired_orders.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} expired orders."))
