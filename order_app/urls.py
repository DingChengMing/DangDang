from django.urls import path

from order_app import views

urlpatterns = [
    path('showPage/', views.show_page, name='showPage'),
    path('queryAddress/', views.query_address, name='queryAddress'),
    path('createOrder/', views.create_order, name='createOrder'),
    path('createItem/', views.create_item, name='createItem'),
    path('addCart/', views.add_cart, name='addCart'),
    path('addAddress/', views.add_address, name='addAddress'),
    path('access/', views.access, name='access'),
]