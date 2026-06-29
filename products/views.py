from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView
from .models import Tag, Product
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ProductForm

# Viste Prodotti
class ProductListView(ListView):
    model = Product
    template_name = "product.html"
    
class ProductDetailView(DetailView):
    model = Product
    template_name = "products/products_detail.html"
    context_object_name = "product"

class ProductUpdateView(UpdateView, UserPassesTestMixin, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = "products/products_update.html"

    def get_success_url(self):
        return self.object.get_absolute_url()
    
    def test_func(self):
        return self.request.user.is_manager()

class ProductDeleteView(DeleteView, UserPassesTestMixin, LoginRequiredMixin):
    model = Product
    template_name = "products/products_delete.html"
    success_url = reverse_lazy("product_list")
    def test_func(self):
        return self.request.user.is_manager()

class ProductCreateView(CreateView, UserPassesTestMixin, LoginRequiredMixin):
    model = Product
    template_name = "products/products_create.html"
    form_class = ProductForm
    success_url = reverse_lazy("product_list")

    def test_func(self):
        return self.request.user.is_manager()

#Viste Tags

class TagListView(TemplateView):
    template_name = "tags.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Tag.objects.all().prefetch_related("product_set")

        context["categories"] = categories
        return context


class TagCreateView(CreateView, UserPassesTestMixin, LoginRequiredMixin):
    model = Tag
    template_name = "products/tag_create.html"
    fields = ["name"]
    success_url = reverse_lazy("tag_list") ##da mettere il link alla pagina delle categorie

    def test_func(self):
        return self.request.user.is_manager()
    
class TagUpdateView(UpdateView, UserPassesTestMixin, LoginRequiredMixin):
    model = Tag
    fields = ["name"]
    template_name = "products/tag_update.html"
    success_url = reverse_lazy("tag_list")
    
    def test_func(self):
        return self.request.user.is_manager()

class TagDeleteView(DeleteView, UserPassesTestMixin, LoginRequiredMixin):
    model = Tag
    template_name = "products/tag_delete.html"
    success_url = reverse_lazy("tag_list")
    def test_func(self):
        return self.request.user.is_manager()