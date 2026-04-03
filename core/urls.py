from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('sales/', views.sales_history, name='sales_history'),
    path('receipt/<int:sale_id>/', views.download_receipt, name='download_receipt'),
    path('daily/', views.daily_sales_pdf, name='daily_sales_pdf'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report/pdf/', views.daily_sales_pdf, name='daily_sales_pdf'),
    path('report/excel/', views.daily_sales_excel, name='daily_sales_excel'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]
