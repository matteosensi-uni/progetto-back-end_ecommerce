from django.urls import path

from .views import HomePageView, ManagerView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("manager/", ManagerView.as_view(), name="manager")
]
