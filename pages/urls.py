# pages/urls.py
from django.urls import path
from .views import homePageView, AboutPageView

urlpatterns = [
    path('about/', AboutPageView.as_view(), name='about'),
    path('', homePageView, name='home'),
]