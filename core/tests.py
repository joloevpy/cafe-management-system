from django.test import TestCase
from .models import Shift, Table, MenuItem, Order, OrderItem


class CafeTests(TestCase):

    def test_shift_create(self):
        shift = Shift.objects.create()
        self.assertTrue(shift.is_open)

    def test_menu_item_create(self):
        item = MenuItem.objects.create(
            name="Lagman",
            price=250
        )
        self.assertEqual(item.name, "Lagman")

    def test_order_total(self):
        shift = Shift.objects.create()

        table = Table.objects.create(
            number=1
        )

        item = MenuItem.objects.create(
            name="Lagman",
            price=250
        )

        order = Order.objects.create(
            shift=shift,
            table=table
        )

        OrderItem.objects.create(
            order=order,
            menu_item=item,
            quantity=2
        )

        order.calculate_total()

        self.assertEqual(
            order.total_price,
            500
        )