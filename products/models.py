from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse

#Mod4llo per le categorie
class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)  
    slug = models.SlugField(blank=True, unique=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

#Modello per i prodotti
class Product(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=255, blank = True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    categories = models.ManyToManyField(Tag)
    slug = models.SlugField(blank=True, unique=True)
    
    def get_absolute_url(self):
        return reverse("product_detail", args=[self.pk, self.slug])    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.price}€) {self.slug}"
    
    def final_price(self):
        return self.price * (1 - self.discount/100)

