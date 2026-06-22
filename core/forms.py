from django import forms
from .models import Order, MenuItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'shift',
            'table',
            'promo_code',
            'status'
        ]

    def save(self, commit=True):
        order = super().save(commit=False)

        if commit:
            order.save()

        order.calculate_total()

        return order


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            'name',
            'price'
        ]

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0")

        return price