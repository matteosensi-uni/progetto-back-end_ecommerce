from django.urls import path

from .views import (ProductListView,
                     ProductDetailView,
                       ProductUpdateView,
                         ProductDeleteView,
                           ProductCreateView,
                             TagCreateView,
                               TagListView,
                                TagUpdateView,
                                 TagDeleteView,
                                  TagDetailView )


urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    # PRODUCTS
    path("products/<int:pk>/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:pk>/<slug:slug>/edit/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/<slug:slug>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    #TAGS
    path("tags/", TagListView.as_view(), name="tag_list"),
    path("tags/<int:pk>/<slug:slug>/edit/", TagUpdateView.as_view(), name="tag_update"),
    path("tags/<int:pk>/<slug:slug>/delete/", TagDeleteView.as_view(), name="tag_delete"),
    path("tags/create/", TagCreateView.as_view(), name="tag_create"),
    path("tags/<slug:slug>/", TagDetailView.as_view(), name="tag_detail")
]
