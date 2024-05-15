from django.urls import path
from new_api import views

urlpatterns = [
    path('crmled', views.get_crmled, name='get_crmled'),
    path('masslm', views.get_mass, name='get_mass'),
    path('calculate_probability', views.calculate_probability, name='calculate_probability'),

]