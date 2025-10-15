from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Clear all fake data from database'

    def handle(self, *args, **options):
        self.stdout.write('Clearing all fake data...')
        
        # Clear data in reverse order of dependencies
        from receipts.models import Receipt
        from payments.models import Payment
        from appointments.models import Appointment
        from leads.models import Lead
        from patients.models import Patient
        from settings.models import Treatment, Doctor
        
        Receipt.objects.all().delete()
        Payment.objects.all().delete()
        Appointment.objects.all().delete()
        Lead.objects.all().delete()
        Patient.objects.all().delete()
        Treatment.objects.all().delete()
        Doctor.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully cleared all fake data!')
        )
