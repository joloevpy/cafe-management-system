from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum

from .models import MenuItem, Shift, Order

def home(request):
    return render(request, 'index.html')

def menu_list(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})

def order_list(request):
    orders = Order.objects.all()

    return render(
        request,
        'orders.html',
        {'orders': orders}
    )


def shift_list(request):
    shifts = Shift.objects.all()

    return render(
        request,
        'shift.html',
        {'shifts': shifts}
    )

def open_shift(request):
    Shift.objects.create(
        is_open=True
    )
    return redirect('shift')
def close_shift(request, shift_id):
    shift = Shift.objects.get(id=shift_id)

    revenue = Order.objects.filter(
        shift=shift,
        status='completed'
    ).aggregate(
        total=Sum('total_price')
    )

    shift.total_revenue = revenue['total'] or 0
    shift.is_open = False
    shift.closed_at = timezone.now()

    shift.save()

    return redirect('shift')