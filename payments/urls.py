from django.urls import path
from . import views


urlpatterns = [
    path('', views.payment_list, name='payments_page'),
    path('create/', views.payment_create, name='payment_create'),
]


