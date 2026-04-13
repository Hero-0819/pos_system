from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Product,Sale,SaleItem
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.utils import timezone
from .models import Sale
from openpyxl import Workbook
from decimal import Decimal
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_superuser

def is_cashier(user):
    return not user.is_superuser

def create_admin(request):
    User.objects.filter(username="admin").delete()

    User.objects.create_superuser(
        username="admin",
        email="cassianshujaa06@gmail.com",
        password="admin123"
    )

    return HttpResponse("admin reset success")
def create_cashier(request):
  if not User.objects.filter(username="cashier").exists():
     User.objects.create_user(
       username="cashier",
       password="1234"
    )
  return HttpResponse("cashier created")
@login_required
@user_passes_test(is_admin)
def dashboard(request):
    today = timezone.localdate()

    sales_today = Sale.objects.filter(created_at__date=today)

    total_sales = sales_today.aggregate(total=Sum('total'))['total'] or 0
    number_of_sales = sales_today.count()
    # 💰 PROFIT CALCULATION
    profit = 0

    for sale in sales_today:
        for item in sale.items.all():
            profit += (item.product.price - item.product.cost_price) * item.qty
    low_stock_products = Product.objects.filter(stock__lte=F('low_stock_threshold'))
    recent_sales = Sale.objects.order_by('-id')[:5]

    return render(request, 'dashboard.html', {
      'total_sales': total_sales,
      'number_of_sales': number_of_sales,
      'profit': profit,
      'low_stock_products': low_stock_products,
      'recent_sales': recent_sales,
})

@login_required
def home(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {}) or {}

    cart_items = []

    for product_id, qty in cart.items():
        try:
            product = Product.objects.filter(id=product_id).first()
            if product:
               cart_items.append({
                 'product': product,
                 'qty': qty,
                 'subtotal': product.price * qty
            })

        except:
            continue

    return render(request, 'home.html', {
        'products': products,
        'cart_items': cart_items
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    product = Product.objects.get(id=product_id)

    current_qty = cart.get(product_id, 0)

    if current_qty < product.stock:
        cart[product_id] = current_qty + 1

    request.session['cart'] = cart
    return redirect('home')
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('home')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('home')

    sale = Sale.objects.create(total=0)
    total = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)

        subtotal = product.price * qty
        total += subtotal

        SaleItem.objects.create(
            sale=sale,
            product=product,
            qty=qty,
            price=product.price,
            subtotal=subtotal
        )

        product.stock -= qty
        product.save()

    sale.total = total
    sale.save()

    request.session['cart'] = {}

    return redirect('download_receipt',sale_id=sale.id)

def sales_history(request):
    sales = Sale.objects.all().order_by('-created_at')

    return render(request, 'sales.html', {
        'sales': sales
    })
from reportlab.pdfgen import canvas
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Sale
@login_required
def download_receipt(request, sale_id):
    sale = Sale.objects.get(id=sale_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{sale.id}.pdf"'

    p = canvas.Canvas(response)

    y = 800

    # 🏪 SHOP NAME
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "SHUJAA STORE")
    y -= 30

    # 🧾 INVOICE
    p.setFont("Helvetica", 12)
    p.drawString(100, y, f"Receipt: {sale.invoice_no}")
    y -= 20

    # 📅 DATE
    p.drawString(100, y, f"Date: {sale.created_at.strftime('%Y-%m-%d %H:%M')}")
    y -= 30

    # LINE
    p.drawString(100, y, "------------------------------")
    y -= 20

    # 🛒 ITEMS
    for item in sale.items.all():
        text = f"{item.product.name} x{item.qty} = {item.subtotal}"
        p.drawString(100, y, text)
        y -= 20

    y -= 10
    p.drawString(100, y, "------------------------------")
    y -= 20

    # 💰 TOTAL
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, f"TOTAL: {sale.total}")

    y -= 40

    # 🙏 FOOTER
    p.setFont("Helvetica", 10)
    p.drawString(100, y, "Thank you for your purchase!")

    p.showPage()
    p.save()

    return response
def daily_sales_pdf(request):
    today = timezone.localdate()
    sales = Sale.objects.filter(created_at__date=today)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="daily_sales_report.pdf"'

    p = canvas.Canvas(response)

    y = 800

    # TITLE
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, y, "DAILY SALES REPORT")
    y -= 30

    p.setFont("Helvetica", 12)
    p.drawString(100, y, f"Date: {today}")
    y -= 30

    p.drawString(100, y, "----------------------------------")
    y -= 20

    total = 0

    for sale in sales:
        text = f"{sale.invoice_no} - {sale.total}"
        p.drawString(100, y, text)
        y -= 20
        total += sale.total

    y -= 10
    p.drawString(100, y, "----------------------------------")
    y -= 20

    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, f"TOTAL SALES: {total}")

    p.showPage()
    p.save()

    return response
def daily_sales_excel(request):
    today = timezone.localdate()
    sales = Sale.objects.filter(created_at__date=today)

    wb = Workbook()
    ws = wb.active
    ws.title = "Daily Sales"

    # HEADER
    ws.append(["Invoice", "Total", "Date"])

    total = 0

    for sale in sales:
        ws.append([
            sale.invoice_no,
            float(sale.total),
            sale.created_at.strftime("%Y-%m-%d %H:%M")
        ])
        total += sale.total

    # SUMMARY ROW
    ws.append([])
    ws.append(["TOTAL", float(total), ""])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="daily_sales.xlsx"'

    wb.save(response)

    return response

