from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.CharField(max_length=100)

    def __str__(self):
        return self.customer_name

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.FloatField()
    digital = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.product_name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_complete = models.BooleanField(default=False)
    tranction_id = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)

    @property
    def total_cart_items_price(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.totalPrice for item in orderitem])
        return total
    @property
    def totalItem(self):
        orderItem = self.orderitem_set.all()
        total = sum(item.totals for item in orderItem)
        return total

    @property
    def shipping(self):
        shipping=False
        orderItem = self.orderitem_set.all()
        for i in orderItem:
            if i.product.digital == False:
                shipping = True
            else:
                shipping = False
        return shipping

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def totalPrice(self):
        total = self.product.price * self.quantity
        return total

    @property
    def totals(self):
        total = self.quantity
        return total
        

class shippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address