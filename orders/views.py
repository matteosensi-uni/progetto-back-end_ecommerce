from django.views import View
from django.views.generic import TemplateView, CreateView, ListView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from .forms import CheckOutForm
from users.models import CustomUser
from .mixins import OrderFilterMixin
from django.contrib import messages

#Cart Views
#Vista della pagina principale del carrello, collegata alla pagina cart.html
class CartView(LoginRequiredMixin, TemplateView):
    model = Cart
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"], _ = Cart.objects.get_or_create(user=self.request.user)
        return context
    
#Vista per aggiungere elementi al carrello, collegata ai form di aggiunta dei prodotti nella pagina product_details.html
class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart, _ = Cart.objects.get_or_create(user=request.user) #se il carrello non esiste ancora viene creato
        quantity = int(request.POST.get("quantity", 1)) #prendo la quantità inserita nel form
        cartItem, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity}) #controllo se l'elemento cartItem è presente nel carrello altrimenti lo creo
        #se il prodotto è presente nel carrello aggiorno la quantità altrimenti la imposto
        if not created:
            cartItem.quantity += quantity
        else:
            cartItem.quantity = quantity
        cartItem.save()
        messages.success( request, f"{product.name} è stato aggiunto al carrello!")
        return redirect( product.get_absolute_url())
    
#Vista per modificare gli elementi del carrello, collegata ai form di modifica dei prodotti nella pagina cart.html
class EditCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cartItem = get_object_or_404(CartItem, pk=pk)
        if cartItem.cart.user != request.user: #controllo che la richiesta sia originata effettivamente dall'utente del carrello
            return redirect("cart_view")
        quantity = int(request.POST.get("quantity", 1))
        cartItem.quantity = quantity
        cartItem.save()
        messages.success( request, f"{cartItem.product.name} è stato modificato correttamente!")
        return redirect("cart_view")
#Vista per rimuovere un elemento dal carrello, collegata al form di eliminazione dei prodotti nella pagina cart.html
class RemoveCartItemView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cartItem = get_object_or_404(CartItem, pk=pk)
        if cartItem.cart.user != request.user: #controllo che la richiesta sia originata effettivamente dall'utente del carrello
            return redirect("cart_view")
        cartItem.delete()
        messages.success( request, f"{cartItem.product.name} è stato rimosso dal carrello!")
        return redirect("cart_view")
    
    

#Order Views
#Vista per il CheckOut
class CheckOutView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = CheckOutForm
    template_name = "orders/checkout.html"

    def form_valid(self, form): #se il form è valido procedo a creare l'ordine
        cart = Cart.objects.get(user=self.request.user)
        order = form.save(commit=False) #creo l'ordine dai dati del form senza però committarlo, altrimenti darebbe errore perché manca l'utente
        order.user = self.request.user
        order.save()
        cartItems = cart.cartitem_set.all() #recupero i prodotti del carrello

        for item in cartItems:
            if(item.quantity > item.product.stock): #controllo la disponibilità dei prodotti
                form.add_error(None, f"Non ci sono abbastanza prodotti per {item.product.name}. Disponibili: {item.product.stock}, Richiesti: {item.quantity}")
                return self.form_invalid(form)
            #creo gli orderItem
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                actual_price_per_unit=item.product.final_price()
            )
            item.product.stock -= item.quantity #aggiorno lo stock dei prodotti acquistati
            item.product.save()

        cartItems.delete()  #elimino i prodotti ordinati dal carrello
        return redirect("order_success")

    def get_initial(self): #imposto i valori di default per i campi del form con i dati dell'utente
        return {
            "email_used": self.request.user.email,
            "order_address": self.request.user.address,
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"], _ = Cart.objects.get_or_create(user=self.request.user)
        return context
    
    def handle_no_permission(self):
            return redirect("home")
    


class OrderSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "orders/order_success.html"

#Vista per gli ordini per l'utente Customer (può solo vedere gli ordini fatti)
class CustomerOrderListView(LoginRequiredMixin, OrderFilterMixin, ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = Order.Status.choices
        return context
    #Gestione dei filtri sui dati da visualizzare
    def get_queryset(self):
        orders = Order.objects.all().filter(user=self.request.user)
        return self.apply_filters(orders)

    def handle_no_permission(self):
            return redirect("home")

#vista per gli ordini per il manager (può vedere gli ordini di tutti gli utenti e modificare il loro stato)
class ManagerOrderListView(LoginRequiredMixin, UserPassesTestMixin, OrderFilterMixin, ListView):
    model = Order
    template_name = "orders/order_management.html"
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = CustomUser.objects.all()
        context["statuses"] = Order.Status.choices
        return context

    #Gestione dei filtri sui dati da visualizzare
    def get_queryset(self):
        orders = Order.objects.all()
        username = self.request.GET.get("user")
        if username:
            orders = orders.filter(user__username=username)
        return self.apply_filters(orders)
    
    #funzione per verificare le permissions dell'utente
    def test_func(self):
        return self.request.user.has_perm("orders.manage_orders")
    
    
#View per modificare lo stato dell'ordine, collegata alla pagina order_management.html
class UpdateOrderStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = request.POST.get("status")
        order.save()
        return redirect("order_management")
    
    #funzione per verificare le permissions dell'utente
    def test_func(self):
        return self.request.user.has_perm("orders.manage_orders")

    