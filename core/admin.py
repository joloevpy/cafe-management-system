from django.contrib import admin
from .models import (
    Shift,
    Table,
    MenuItem,
    Order,
    PromoCode,
    OrderItem
)

admin.site.register(Shift)
admin.site.register(Table)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(PromoCode)
admin.site.register(OrderItem)