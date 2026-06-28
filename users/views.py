from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from django.shortcuts import render

from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from django.contrib.auth.models import Group

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
    def form_valid(self, form):  #Assegno il gruppo Customer alla creazione dell'utente, un utente manager può essere impostato solo dalla pagina admin
        response = super().form_valid(form)   # salva utente
        group = Group.objects.get(name="Customer")
        self.object.groups.add(group)
        return response

    

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("edit_profile")
    template_name = "edit_profile.html"
    
    def get_object(self):
        return self.request.user


class MyLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("home")