from django.urls import path

from .views import (
    home,
    menu_list,
    MenuItemCreateView,
    OrderListView,
    OrderCreateView,
    shift_list,
    open_shift,
    close_shift,
    promo_code_list,
    PromoCodeCreateView,
    table_list,
    TableCreateView,
)

urlpatterns = [
    path('', home, name='home'),

    path('menu/', menu_list, name='menu'),
    path('menu/create/', MenuItemCreateView.as_view(), name='create_menu_item'),

    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/create/', OrderCreateView.as_view(), name='create_order'),

    path('shift/', shift_list, name='shift'),
    path('shift/open/', open_shift, name='open_shift'),
    path('shift/close/<int:shift_id>/', close_shift, name='close_shift'),

    path('promocodes/', promo_code_list, name='promo_codes'),
    path(
        'promocodes/create/',
        PromoCodeCreateView.as_view(),
        name='create_promo_code'
    ),

    path('tables/', table_list, name='tables'),
    path(
        'tables/create/',
        TableCreateView.as_view(),
        name='create_table'
    ),
]