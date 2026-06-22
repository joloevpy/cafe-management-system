from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from .models import MenuItem, Shift, Order, PromoCode
from .forms import OrderForm, MenuItemForm




class OrderListView(ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'create_order.html'
    success_url = reverse_lazy('orders')


class MenuItemCreateView(CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'create_menu_item.html'
    success_url = reverse_lazy('menu')



def home(request):
    promo_codes = PromoCode.objects.all()

    return render(request, 'index.html', {
        'promo_codes': promo_codes
    })


def menu_list(request):
    menu_items = MenuItem.objects.all()

    return render(request, 'menu.html', {
        'menu_items': menu_items
    })


def shift_list(request):
    shifts = Shift.objects.all()

    return render(request, 'shift.html', {
        'shifts': shifts
    })



def open_shift(request):
    if request.method == "POST":
        Shift.objects.create(is_open=True)

    return redirect('shift')


def close_shift(request, shift_id):
    if request.method != "POST":
        return redirect('shift')

    shift = get_object_or_404(Shift, id=shift_id)

    revenue = Order.objects.filter(
        shift=shift,
        status='completed'
    ).aggregate(total=Sum('total_price'))

    total_revenue = revenue.get("total") or 0

    shift.total_revenue = total_revenue
    shift.is_open = False
    shift.closed_at = timezone.now()
    shift.save()

    return redirect('shift')