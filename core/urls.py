from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Note: Keeping your specific view imports as requested
from .views import create_admin, create_cashier

urlpatterns = [
    # --- POS / Cashier Routes ---
    path('', views.home, name='home'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # --- Sales & Receipts ---
    path('sales/', views.sales_history, name='sales_history'),
    path('receipt/<int:sale_id>/', views.download_receipt, name='download_receipt'),
    
    # --- Admin & Analytics ---
    # This matches the link in the new Sidebar/Navbar UI
    path('admin_dashboard/', views.dashboard, name='admin_dashboard'), 
    path('dashboard/', views.dashboard, name='dashboard'), # Duplicate for safety
    
    # --- Reports ---
    path('daily/', views.daily_sales_pdf, name='daily_sales_pdf'),
    path('report/pdf/', views.daily_sales_pdf, name='daily_sales_pdf_alt'),
    path('report/excel/', views.daily_sales_excel, name='daily_sales_excel'),
    
    # --- Authentication ---
    # Using Django's built-in logout view
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # --- Setup / Utility ---
    path('create-admin/', create_admin, name='create_admin'),
    path('create-cashier/', create_cashier, name='create_cashier'),
]
