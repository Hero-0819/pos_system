from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    stock = models.IntegerField()
    low_stock_threshold = models.IntegerField(default=5)

    def __str__(self):
        return self.name

class Sale(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(default=0)
    invoice_no = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.invoice_no} - {self.total}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()

    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
