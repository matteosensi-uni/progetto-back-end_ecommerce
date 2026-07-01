from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView
from .models import Tag, Product
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ProductForm
from django.db.models import Q
from django.shortcuts import redirect

# Viste Prodotti
class ProductListView(ListView):
    model = Product
    template_name = "product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Tag.objects.all()
        context["categories"] = categories
        return context

    def get_queryset(self):
        queryset = Product.objects.all()
        name = self.request.GET.get("q")
        category = self.request.GET.get("category")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if name:
            queryset = queryset.filter(
                Q(name__icontains=name) |
                Q(description__icontains=name)
            )
        if category:
            queryset = queryset.filter(categories__id=category)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset.distinct()


    
class ProductDetailView(DetailView):
    model = Product
    template_name = "products/products_detail.html"
    context_object_name = "product"

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/products_update.html"

    def get_success_url(self):
        return self.object.get_absolute_url()
    
    def test_func(self):
        return self.request.user.has_perm("products.change_product")
    
    def handle_no_permission(self):
            return redirect("home")

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "products/products_delete.html"
    success_url = reverse_lazy("product_list")
    def test_func(self):
        return self.request.user.has_perm("products.delete_product")
    
    def handle_no_permission(self):
            return redirect("home")

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    template_name = "products/products_create.html"
    form_class = ProductForm
    success_url = reverse_lazy("product_list")

    def test_func(self):
        return self.request.user.has_perm("products.create_product")
    
    def handle_no_permission(self):
            return redirect("home")

#Viste Tags

class TagListView(TemplateView):
    template_name = "tags.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Tag.objects.all().prefetch_related("product_set")

        context["categories"] = categories
        return context


class TagCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Tag
    template_name = "products/tag_create.html"
    fields = ["name"]
    success_url = reverse_lazy("tag_list") ##da mettere il link alla pagina delle categorie

    def test_func(self):
        return self.request.user.has_perm("products.create_tag")
    
    def handle_no_permission(self):
            return redirect("home")
    
class TagUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tag
    fields = ["name"]
    template_name = "products/tag_update.html"
    success_url = reverse_lazy("tag_list")
    
    def test_func(self):
        return self.request.user.has_perm("products.change_tag")

class TagDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tag
    template_name = "products/tag_delete.html"
    success_url = reverse_lazy("tag_list")
    def test_func(self):
        return self.request.user.has_perm("products.delete_tag")
    
    def handle_no_permission(self):
            return redirect("home")
    
class TagDetailView(DetailView):
    model = Tag
    template_name = "products/tag_detail.html"
    context_object_name = "category"