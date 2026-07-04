from django import forms
from .models import Product

#Form per Creare/Modificare un prodotto
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "discount", "categories"]

        widgets = {
            "categories": forms.CheckboxSelectMultiple(),
        }