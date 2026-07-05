from django.views.generic import TemplateView
from products.models import Product, Tag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

#Vista per la home page del sito
class HomePageView(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Tag.objects.all()
        context["discount_products"] = Product.objects.filter(discount__gt=0)[:8]
        return context
    
#Vista per la pagina manager
class ManagerView(LoginRequiredMixin, UserPassesTestMixin , TemplateView):
    template_name = "manager.html"

    def test_func(self):
        return self.request.user.is_manager()
