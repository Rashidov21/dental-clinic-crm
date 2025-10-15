from django.core.management.base import BaseCommand
from django.utils import translation
from settings.models import Doctor, Treatment
from leads.models import Lead
from patients.models import Patient
from appointments.models import Appointment
from payments.models import Payment
from receipts.models import Receipt

class Command(BaseCommand):
    help = 'Populates the database with translated content for all models'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Populating translations...'))
        
        # Doctor translations
        doctors = Doctor.objects.all()
        for doctor in doctors:
            # Set Uzbek translations
            doctor.name_uz = doctor.name
            doctor.specialization_uz = doctor.specialization
            
            # Set Russian translations
            doctor.name_ru = doctor.name
            doctor.specialization_ru = doctor.specialization
            
            # Set Uzbek Cyrillic translations
            doctor.name_uz_cyrl = doctor.name
            doctor.specialization_uz_cyrl = doctor.specialization
            
            doctor.save()
        
        self.stdout.write(self.style.SUCCESS(f'Updated {doctors.count()} doctors'))
        
        # Treatment translations
        treatments = Treatment.objects.all()
        for treatment in treatments:
            # Set Uzbek translations
            treatment.name_uz = treatment.name
            treatment.description_uz = treatment.description
            
            # Set Russian translations
            treatment.name_ru = treatment.name
            treatment.description_ru = treatment.description
            
            # Set Uzbek Cyrillic translations
            treatment.name_uz_cyrl = treatment.name
            treatment.description_uz_cyrl = treatment.description
            
            treatment.save()
        
        self.stdout.write(self.style.SUCCESS(f'Updated {treatments.count()} treatments'))
        
        # Lead translations
        leads = Lead.objects.all()
        for lead in leads:
            # Set Uzbek translations
            lead.full_name_uz = lead.full_name
            lead.source_uz = lead.source
            lead.notes_uz = lead.notes
            
            # Set Russian translations
            lead.full_name_ru = lead.full_name
            lead.source_ru = lead.source
            lead.notes_ru = lead.notes
            
            # Set Uzbek Cyrillic translations
            lead.full_name_uz_cyrl = lead.full_name
            lead.source_uz_cyrl = lead.source
            lead.notes_uz_cyrl = lead.notes
            
            lead.save()
        
        self.stdout.write(self.style.SUCCESS(f'Updated {leads.count()} leads'))
        
        # Patient translations
        patients = Patient.objects.all()
        for patient in patients:
            # Set Uzbek translations
            patient.full_name_uz = patient.full_name
            patient.address_uz = patient.address
            patient.notes_uz = patient.notes
            
            # Set Russian translations
            patient.full_name_ru = patient.full_name
            patient.address_ru = patient.address
            patient.notes_ru = patient.notes
            
            # Set Uzbek Cyrillic translations
            patient.full_name_uz_cyrl = patient.full_name
            patient.address_uz_cyrl = patient.address
            patient.notes_uz_cyrl = patient.notes
            
            patient.save()
        
        self.stdout.write(self.style.SUCCESS(f'Updated {patients.count()} patients'))
        
        # Appointment translations
        appointments = Appointment.objects.all()
        for appointment in appointments:
            # Set Uzbek translations
            appointment.doctor_name_uz = appointment.doctor_name
            appointment.service_uz = appointment.service
            appointment.notes_uz = appointment.notes
            
            # Set Russian translations
            appointment.doctor_name_ru = appointment.doctor_name
            appointment.service_ru = appointment.service
            appointment.notes_ru = appointment.notes
            
            # Set Uzbek Cyrillic translations
            appointment.doctor_name_uz_cyrl = appointment.doctor_name
            appointment.service_uz_cyrl = appointment.service
            appointment.notes_uz_cyrl = appointment.notes
            
            appointment.save()
        
        self.stdout.write(self.style.SUCCESS(f'Updated {appointments.count()} appointments'))
        
        # Payment translations
        payments = Payment.objects.all()
        for payment in payments:
            # Set Uzbek translations
            payment.notes_uz = payment.notes
            
            # Set Russian translations
            payment.notes_ru = payment.notes
            
            # Set Uzbek Cyrillic translations
            payment.notes_uz_cyrl = payment.notes
            
            payment.save()
        
        self.stdout.write(self.style.SUCCESS(f'Updated {payments.count()} payments'))
        
        # Receipt translations
        receipts = Receipt.objects.all()
        for receipt in receipts:
            # Set Uzbek translations
            receipt.services_done_uz = receipt.services_done
            
            # Set Russian translations
            receipt.services_done_ru = receipt.services_done
            
            # Set Uzbek Cyrillic translations
            receipt.services_done_uz_cyrl = receipt.services_done
            
            receipt.save()
        
        self.stdout.write(self.style.SUCCESS(f'Updated {receipts.count()} receipts'))
        
        self.stdout.write(self.style.SUCCESS('Successfully populated all translations!'))
