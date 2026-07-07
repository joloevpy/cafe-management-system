from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from.models import MenuItem, Shift, Order, PromoCode, Table, OrderItem
from.forms import OrderForm, MenuItemForm

class OrderListView(ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'create_order.html'
    success_url = reverse_lazy('orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = MenuItem.objects.all()
        return context

    def form_valid(self, form):
        shift = Shift.get_active()
        if not shift:
            form.add_error(None, "No active shift")
            return self.form_invalid(form)

        form.instance.shift = shift
        order = form.save()

        menu_items = self.request.POST.getlist('menu_item')
        quantities = self.request.POST.getlist('quantity')

        if not menu_items or menu_items[0] == '':
            form.add_error(None, "Заказ бош болбош керек")
            order.delete()
            return self.form_invalid(form)

        for i in range(len(menu_items)):
            if menu_items[i]:
                OrderItem.objects.create(
                    order=order,
                    menu_item_id=menu_items[i],
                    quantity=quantities[i]
                )

        return redirect(self.success_url)

class MenuItemCreateView(CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'create_menu_item.html'
    success_url = reverse_lazy('menu')

def home(request):
    return render(request, 'index.html')

def menu_list(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})

def shift_list(request):
    shifts = Shift.objects.all()
    return render(request, 'shift.html', {'shifts': shifts})

def open_shift(request):
    if request.method == "POST":
        if Shift.objects.filter(is_open=True).exists():
            return redirect('shift')
        Shift.objects.create(is_open=True)
    return redirect('shift')

def close_shift(request, shift_id):
    if request.method!= "POST":
        return redirect('shift')

    shift = get_object_or_404(Shift, id=shift_id)
    if shift.is_open is False:
        return redirect('shift')

    revenue = Order.objects.filter(
        shift=shift,
        status='completed'
    ).aggregate(total=Sum('total_price'))

    shift.total_revenue = revenue.get("total") or 0
    shift.is_open = False
    shift.closed_at = timezone.now()
    shift.save()
    return redirect('shift')