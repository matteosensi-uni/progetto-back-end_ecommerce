from django.db import models
from django.core.validators import MinValueValidator

#Cart model
class Cart(models.Model):
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE)
    
    #funzione che calcola il prezzo totale del carrello
    def get_total_price(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.total_price()
        return total
    
    def __str__(self):
        return f"Cart of {self.user.username}"

#CartItem model, modello per gli elementi del carrello
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=False, null=False)    

    #funzione che calcola il prezzo per ogni prodotto del carrello (prezzo per unità * quantità)
    def total_price(self):
            return self.product.final_price() * self.quantity

    def __str__(self):
        return f"{self.product.name} x{self.quantity} (Cart {self.cart.id})"
    
#Order model
class Order(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True) #imposto on_delete=models.SET_NULL e null=True in modo da tenere gli ordini di un utente eliminato 
    email_used = models.EmailField()                    #non uso l'email dell'utente perché l'utente può scegliere di usare un'altra e-mail per l'ordine
    order_address = models.CharField(max_length=255)    #stessa cosa della e-mail
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Status(models.TextChoices):   #classe per lo stato del prodotto
        ORDERED = "ORDERED", "Ordinato"
        DELIVERED = "DELIVERED", "Consegnato"
        PROCESSING = "PROCESSING", "In Elaborazione"
    
    class Meta:
        permissions = [
            ("manage_orders", "Can manage orders"), #permissions personalizzate per gli ordini
        ]
        ordering = ["user__username", "-created_at"] #ordinamento per gli ordini in base alla data di creazione e dell'utente (quest'ultimo ordinamento serve per la pagina managers)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ORDERED,
    )
    #Calcolo del totale dell'ordine
    def get_total_price(self):
        total = 0
        for item in self.orderitem_set.all():
            total += item.total_price()
        return total

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.get_total_price()}€"

#OrderItem model, modello per gli elementi dell'ordine
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True) #imposto on_delete=models.SET_NULL e null=True in modo da tenere gli orderItem di un prodotto eliminato
    quantity = models.PositiveIntegerField(blank=False, null=False)
    actual_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]) #si usa un attributo per il salvare prezzo in quanto il prezzo dei 
                                                                                                                    #  singoli prodotti potrebbe variare nel tempo
    #calcolo del prezzo per ogni prodotto in funzione della quantità
    def total_price(self):
            return self.actual_price_per_unit * self.quantity

    def __str__(self):
        return f"{self.product.name} x{self.quantity} (Order {self.order.id})"

    