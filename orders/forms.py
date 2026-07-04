from django.forms import ModelForm
from .models import Order

#Form per il CheckOut, si richiede
#   - email per il check-out (che può essere diversa da quella dell'utente)
#   - indirizzo di spedizione (che può essere diverso da quello inserito durante la registrazione)
class CheckOutForm(ModelForm):
    class Meta:
        model = Order
        fields = ['email_used', 'order_address']