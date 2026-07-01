from django.urls import path

from .views import AddToCartView, CartView, EditCartView, RemoveCartItemView


urlpatterns = [
    path("cart/add/<int:pk>/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart/edit/<int:pk>/", EditCartView.as_view(), name="edit_cart"),
    path("cart/delete/<int:pk>/", RemoveCartItemView.as_view(), name="remove_cart_item"),
    path("cart/", CartView.as_view(), name="cart_view"),
]
