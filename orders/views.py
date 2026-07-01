from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Product
from .models import Cart, CartItem

class CartView(LoginRequiredMixin, TemplateView):
    model = Cart
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)

        total = 0
        for item in cart.cartitem_set.all():
            total += item.product.final_price() * item.quantity
        context["cart"] = cart
        context["total_price"] = total

        return context



class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        quantity = int(request.POST.get("quantity", 1))
        cartItem, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})
        if not created:
            cartItem.quantity += quantity
        else:
            cartItem.quantity = quantity
        
        cartItem.save()
        return redirect( product.get_absolute_url())
    
class EditCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cartItem = get_object_or_404(CartItem, pk=pk)
        if cartItem.cart.user != request.user:
            return redirect("cart_view")
        quantity = int(request.POST.get("quantity", 1))
        cartItem.quantity = quantity
        cartItem.save()
        return redirect("cart_view")
    
class RemoveCartItemView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cartItem = get_object_or_404(CartItem, pk=pk)
        if cartItem.cart.user != request.user:
            return redirect("cart_view")
        cartItem.delete()
        return redirect("cart_view")
    