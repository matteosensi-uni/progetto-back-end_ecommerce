from django.urls import path

from .views import (AddToCartView,
                     CartView,
                       EditCartView,
                         RemoveCartItemView,
                           CheckOutView,
                             OrderSuccessView,
                               CustomerOrderListView,
                                 ManagerOrderListView,
                                 UpdateOrderStatusView
                                 )


urlpatterns = [
    path("cart/add/<int:pk>/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart/edit/<int:pk>/", EditCartView.as_view(), name="edit_cart"),
    path("cart/delete/<int:pk>/", RemoveCartItemView.as_view(), name="remove_cart_item"),
    path("cart/", CartView.as_view(), name="cart_view"),
    path("cart/checkout", CheckOutView.as_view(), name="check_out"),
    path("cart/order_success", OrderSuccessView.as_view(), name="order_success"),
    path("", CustomerOrderListView.as_view(), name="order_list"),
    path("manager/", ManagerOrderListView.as_view(), name="order_management"),
    path("manager/edit/<int:pk>", UpdateOrderStatusView.as_view(), name="status_update"),
]
