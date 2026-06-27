from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError


class Shift(models.Model):
    is_open = models.BooleanField(default=True)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Shift {self.id}"

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_open=True).first()

    @classmethod
    def has_active_shift(cls):
        return cls.objects.filter(is_open=True).exists()


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

    def clean(self):
        if self.discount_percent > 100:
            raise ValidationError(
                {
                    "discount_percent":
                    "Discount cannot exceed 100%"
                }
            )

    def __str__(self):
        return self.name


class Order(models.Model):

    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "progress", "In Progress"
        COMPLETED = "completed", "Completed"

    shift = models.ForeignKey(
        Shift,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    table = models.ForeignKey(
        Table,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def calculate_total(self):
        total = Decimal("0.00")

        for item in self.items.all():
            total += (
                item.menu_item.price *
                item.quantity
            )

        discount = Decimal("0.00")

        if self.promo_code:
            discount = (
                total *
                Decimal(
                    self.promo_code.discount_percent
                ) /
                Decimal("100")
            )

        self.total_price = total - discount

        Order.objects.filter(
            pk=self.pk
        ).update(
            total_price=self.total_price
        )

    def clean(self):
        if (
            self.shift_id and
            not self.shift.is_open
        ):
            raise ValidationError(
                "Cannot create order in closed shift"
            )

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    @property
    def subtotal(self):
        return (
            self.menu_item.price *
            self.quantity
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.calculate_total()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        order.calculate_total()

    def __str__(self):
        return (
            f"{self.menu_item.name} x "
            f"{self.quantity}"
        )