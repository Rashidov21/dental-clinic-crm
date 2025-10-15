from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('test-translations/', TemplateView.as_view(template_name='test_translations.html'), name='test_translations'),
    path('test-notifications/', TemplateView.as_view(template_name='test_notifications.html'), name='test_notifications'),
    path('', include('accounts.urls')),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # UI pages
    path('dashboard/', TemplateView.as_view(template_name='index.html'), name='dashboard_page'),
    path('leads/page/', include('leads.urls')),
    path('calendar/', TemplateView.as_view(template_name='calendar.html'), name='calendar_page'),
    path('clients/', TemplateView.as_view(template_name='clients.html'), name='clients_page'),
    path('payments/page/', TemplateView.as_view(template_name='payments.html'), name='payments_page'),
    path('book/', TemplateView.as_view(template_name='doctor-appointment.html'), name='book_page'),
    path('doctor/', TemplateView.as_view(template_name='doctor-dashboard.html'), name='doctor_page'),
    path('patient/page/', TemplateView.as_view(template_name='patient.html'), name='patient_page'),
    path('receipt/page/', TemplateView.as_view(template_name='receipt.html'), name='receipt_page'),

    # JSON endpoints
    path('', include('dashboard.urls')),
    path('leads/', include('leads.urls')),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('payments/', include('payments.urls')),
    path('receipts/', include('receipts.urls')),
]


