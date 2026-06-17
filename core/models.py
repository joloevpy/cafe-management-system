from django.db import models


class Shift(models.Model):
    is_open = models.BooleanField(default=True)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    total_revenue = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Shift {self.id}"


class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Table {self.number}"


class MenuItem(models.Model):
    name = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    name = models.CharField(max_length=50)
    discount_percent = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):

    STATUS_CHOICES = [
        ("new", "New"),
        ("progress", "In Progress"),
        ("completed", "Completed"),
    ]

    shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE
    )

    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE
    )

    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def calculate_total(self):
        total = 0

        for item in self.orderitem_set.all():
            total += item.menu_item.price * item.quantity

        self.total_price = total
        self.save()

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.menu_item.name}"