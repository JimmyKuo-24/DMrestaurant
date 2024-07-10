from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("gourmet/", views.gourmet, name="gourmet"),
    path("cook/", views.cook, name="cook"),
    path('order/', views.order, name='order'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order_increase/<int:order_id>/', views.order_increase, name='order_increase'),
    path('order_decrease/<int:order_id>/', views.order_decrease, name='order_decrease'),
    path('order_delete/<int:order_id>/', views.order_delete, name='order_delete'),
    path('order_confirm/<int:order_id>/', views.order_confirm, name='order_confirm'),
    path('add_item_to_order/<int:order_id>/', views.add_item_to_order, name='add_item_to_order'),
]