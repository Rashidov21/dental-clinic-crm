from django.urls import path
from . import views


urlpatterns = [
    path('', views.patient_list, name='clients_page'),
    path('<int:pk>/', views.patient_detail, name='patient_page'),
    path('<int:pk>/update/', views.patient_update, name='patient_update'),
    path('<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('create-with-booking/', views.patient_create_with_booking, name='patient_create_with_booking'),
]


