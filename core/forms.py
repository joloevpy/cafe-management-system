from django import forms
from .models import Order, MenuItem, Shift



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'table',
            'promo_code',
            'status'
        ] 

    def clean(self):
        cleaned_data = super().clean()

        shift = Shift.get_active()
        if not shift:
            raise forms.ValidationError("No active shift")

        return cleaned_data

    def save(self, commit=True):
        order = super().save(commit=False)

      
        order.shift = Shift.get_active()

        if commit:
            order.save()

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

        if price is None or price <= 0:
            raise forms.ValidationError("Price must be greater than 0")

        return price