from django.urls import path
from . import views


urlpatterns = [
    path('', views.settings_page, name='settings_page'),
    
    # Doctor management
    path('doctors/create/', views.doctor_create, name='doctor_create'),
    path('doctors/<int:pk>/update/', views.doctor_update, name='doctor_update'),
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),
    
    # Treatment management
    path('treatments/create/', views.treatment_create, name='treatment_create'),
    path('treatments/<int:pk>/update/', views.treatment_update, name='treatment_update'),
    path('treatments/<int:pk>/delete/', views.treatment_delete, name='treatment_delete'),
]
