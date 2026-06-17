from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('menu/', menu_list, name='menu'),
    path('orders/', order_list, name='orders'),
    path('shift/', shift_list, name='shift'),
    path('shift/open/', open_shift, name='open_shift'),
    path('shift/close/<int:shift_id>/', close_shift, name='close_shift'),
]