from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from appointments import views as appointment_views
from dashboard import views as dashboard_views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('test-translations/', TemplateView.as_view(template_name='test_translations.html'), name='test_translations'),
    path('test-notifications/', TemplateView.as_view(template_name='test_notifications.html'), name='test_notifications'),
    path('test-favicon/', TemplateView.as_view(template_name='test_favicon.html'), name='test_favicon'),
    path('test-modals/', TemplateView.as_view(template_name='test_modals.html'), name='test_modals'),
    path('debug-modals/', TemplateView.as_view(template_name='debug_modals.html'), name='debug_modals'),
    path('simple-modal-test/', TemplateView.as_view(template_name='simple_modal_test.html'), name='simple_modal_test'),
    path('', include('accounts.urls')),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # UI pages
    path('dashboard/', include('dashboard.urls')),
    path('leads/page/', include('leads.urls')),
    path('calendar/', include('appointments.urls')),
    path('clients/', include('patients.urls')),
    path('payments/page/', include('payments.urls')),
    path('book/', appointment_views.book_page, name='book_page'),
    path('doctor/', dashboard_views.doctor_dashboard, name='doctor_page'),
    path('patient/page/', include('patients.urls')),
    path('receipt/page/', TemplateView.as_view(template_name='receipt.html'), name='receipt_page'),
    path('settings/', include('settings.urls')),

    # API endpoints
    path('appointments/', include('appointments.urls')),
    path('receipts/', include('receipts.urls')),
    
    # Book appointment endpoints
    path('book/create/', appointment_views.appointment_create, name='book_create'),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


