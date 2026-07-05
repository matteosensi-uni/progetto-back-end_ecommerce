from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView
from .models import Tag, Product
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ProductForm
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.text import slugify
from django.contrib import messages

# Viste Prodotti
#Vista per la visualizzazione della lista completa dei prodotti (oppure con i filtri)
class ProductListView(ListView):
    model = Product
    template_name = "product.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Tag.objects.all()
        return context

    # gestione filtri sui prodotti
    def get_queryset(self):
        products = Product.objects.all()
        name = self.request.GET.get("name")
        if name:
            products = products.filter( Q(name__icontains=name) | Q(description__icontains=name))
        
        category = self.request.GET.get("category")
        if category:
            products = products.filter(categories__id=category)
        
        min_price = self.request.GET.get("min_price")
        if min_price:
            products = products.filter(price__gte=min_price)
        
        max_price = self.request.GET.get("max_price")
        if max_price:
            products = products.filter(price__lte=max_price)
        return products.distinct()

#vista per la pagina prodotto    
class ProductDetailView(DetailView):
    model = Product
    template_name = "products/products_detail.html"
    context_object_name = "product"

#Vista per aggiornare un prodotto
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/products_update.html"

    def form_valid(self, form):
         messages.success(self.request, "Il prodotto è stato aggiornato correttamente!")
         return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
    
    def test_func(self):
        return self.request.user.has_perm("products.change_product")

    def handle_no_permission(self):
            return redirect("home")
    
#Vista per eliminare un prodotto
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "products/products_delete.html"
    success_url = reverse_lazy("product_list")
    def test_func(self):
        return self.request.user.has_perm("products.delete_product")
    
    def handle_no_permission(self):
            return redirect("home")

    def form_valid(self, form):
         messages.success(self.request, "Il prodotto è stato eliminato correttamente!")
         return super().form_valid(form)
    
#Vista per creare un prodotto
class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    template_name = "products/products_create.html"
    form_class = ProductForm
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
         messages.success(self.request, "Il prodotto è stato creato correttamente!")
         return super().form_valid(form)

    def test_func(self):
        return self.request.user.has_perm("products.create_product")
    
    def handle_no_permission(self):
            return redirect("home")

#Viste Tags
#Vista per la visualizzazione delle categorie
class TagListView(ListView):
    template_name = "tags.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Tag.objects.all().prefetch_related("product_set")

#Vista per la visualizzazione delle categorie con i prodotti associati
class TagCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Tag
    template_name = "products/tag_create.html"
    fields = ["name"]
    success_url = reverse_lazy("tag_list")

    #Controllo sul nome della categoria
    def form_valid(self, form):
        slug = slugify(form.cleaned_data["name"])
        if Tag.objects.filter(slug=slug).exists():
            form.add_error( "name", "Esiste già un tag con questo nome.")
            return self.form_invalid(form)
        messages.success(self.request, "La categoria è stata aggiunta correttamente!")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.has_perm("products.create_tag")
    
    def handle_no_permission(self):
            return redirect("home")

#Vista per modifivare il nome di una categoria 
class TagUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tag
    fields = ["name"]
    template_name = "products/tag_update.html"
    success_url = reverse_lazy("tag_list")
    
    #Controllo sul nome della categoria
    def form_valid(self, form):
        slug = slugify(self.object.name)
        if Tag.objects.filter(slug=slug).exclude(pk=self.object.pk).exists():
            form.add_error( "name", "Esiste già un tag con questo nome.")
            return self.form_invalid(form)
        messages.success(self.request, "La categoria è stata aggiornata correttamente!")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.has_perm("products.change_tag")
    
    def handle_no_permission(self):
            return redirect("home")

#Vista per eliminare una categoria
class TagDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tag
    template_name = "products/tag_delete.html"
    success_url = reverse_lazy("tag_list")
    def test_func(self):
        return self.request.user.has_perm("products.delete_tag")
    
    def handle_no_permission(self):
            return redirect("home")
    
    def form_valid(self, form):
        messages.success(self.request, "La categoria è stata eliminata correttamente!")
        return super().form_valid(form)

#Vista per la visualizzazione della singola categoria con i prodotti associati
class TagDetailView(DetailView):
    model = Tag
    template_name = "products/tag_detail.html"
    context_object_name = "category"