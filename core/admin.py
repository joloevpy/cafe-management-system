from django.contrib import admin
from .models import (
    Shift,
    Table,
    MenuItem,
    Order,
    PromoCode,
    OrderItem,
)


admin.site.register(Shift)
admin.site.register(Table)
admin.site.register(MenuItem)
admin.site.register(PromoCode)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "table",
        "status",
        "total_price",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "total_price",
    )

    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        if not obj.shift_id:
            obj.shift = Shift.get_active()

        super().save_model(
            request,
            obj,
            form,
            change
        )