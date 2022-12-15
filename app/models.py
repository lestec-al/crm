from django.db import models
from django.contrib.auth.models import User # to settings.py ???


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.name


class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.sale} - {self.quantity} - {self.product}"


class Sale(models.Model):
    SALE_STAGES_CHOICES = [
        ('r', 'Request'),
        ('p', 'Pack'),
        ('d', 'Delivery'),
        ('f', 'Finished'),
        ('c', 'Canceled'),
    ]
    id = models.BigAutoField(primary_key=True)
    stage = models.CharField(max_length=100, choices=SALE_STAGES_CHOICES, default='r')
    client_name = models.CharField(max_length=100, null=True, blank=True)
    client_address = models.TextField(null=True, blank=True)
    manager = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    products = models.ManyToManyField(Product, through='ProductQuantity')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def total_price(self):
        total_price = 0
        for i in self.products.all():
            total_price += i.price * ProductQuantity.objects.get(product=i, sale=self).quantity
        return total_price

    def __str__(self):
        return f'Sale №{self.id}'


class AdditionalField(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return f'№{self.id} - sale №{self.sale.id}'