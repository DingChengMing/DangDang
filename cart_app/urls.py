from django.urls import path, include

from cart_app import views

urlpatterns = [
    path('showPage/', views.showPage, name='showPage'),
    path('addCart/', views.addCart, name='addCart'),
    path('updateCart/', views.updateCart, name='updateCart'),
    path('delCart/', views.delCart, name='delCart'),
    path('delPart/', views.delPart, name='delPart'),
]
