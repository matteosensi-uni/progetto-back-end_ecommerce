from django.db import models
from django.core.validators import MinValueValidator

class Cart(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])    

    def __str__(self):
        return f"{self.product.name} x{self.quantity} (Cart {self.cart.id})"


class Order(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)], blank = False)    
    
    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.total_price}€"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False ,validators=[MinValueValidator(1)])
    actual_price_per_unit = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)]) 

    def __str__(self):
        return f"{self.product.name} x{self.quantity} (Order {self.order.id})"

    