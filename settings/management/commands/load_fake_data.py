from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random
from decimal import Decimal

from settings.models import Doctor, Treatment
from patients.models import Patient
from leads.models import Lead
from appointments.models import Appointment
from payments.models import Payment
from receipts.models import Receipt


class Command(BaseCommand):
    help = 'Load fake data into all database tables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading fake data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()
        
        self.stdout.write('Loading fake data...')
        
        # Load data in order of dependencies
        self.load_doctors()
        self.load_treatments()
        self.load_patients()
        self.load_leads()
        self.load_appointments()
        self.load_payments()
        self.load_receipts()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded fake data!')
        )

    def clear_data(self):
        """Clear all existing data"""
        Receipt.objects.all().delete()
        Payment.objects.all().delete()
        Appointment.objects.all().delete()
        Lead.objects.all().delete()
        Patient.objects.all().delete()
        Treatment.objects.all().delete()
        Doctor.objects.all().delete()

    def load_doctors(self):
        """Load fake doctors data"""
        doctors_data = [
            {
                'name': 'Dr. Emily Carter',
                'specialization': 'General Dentistry',
                'phone': '+1-555-0101',
                'email': 'emily.carter@dentalclinic.com',
                'is_active': True
            },
            {
                'name': 'Dr. Daniel Lee',
                'specialization': 'Orthodontics',
                'phone': '+1-555-0102',
                'email': 'daniel.lee@dentalclinic.com',
                'is_active': True
            },
            {
                'name': 'Dr. Arjun Patel',
                'specialization': 'Oral Surgery',
                'phone': '+1-555-0103',
                'email': 'arjun.patel@dentalclinic.com',
                'is_active': True
            },
            {
                'name': 'Dr. Sarah Johnson',
                'specialization': 'Periodontics',
                'phone': '+1-555-0104',
                'email': 'sarah.johnson@dentalclinic.com',
                'is_active': True
            },
            {
                'name': 'Dr. Michael Chen',
                'specialization': 'Endodontics',
                'phone': '+1-555-0105',
                'email': 'michael.chen@dentalclinic.com',
                'is_active': True
            },
            {
                'name': 'Dr. Lisa Rodriguez',
                'specialization': 'Pediatric Dentistry',
                'phone': '+1-555-0106',
                'email': 'lisa.rodriguez@dentalclinic.com',
                'is_active': True
            },
            {
                'name': 'Dr. James Wilson',
                'specialization': 'Prosthodontics',
                'phone': '+1-555-0107',
                'email': 'james.wilson@dentalclinic.com',
                'is_active': False  # Inactive doctor
            }
        ]
        
        for doctor_data in doctors_data:
            Doctor.objects.get_or_create(
                name=doctor_data['name'],
                defaults=doctor_data
            )
        
        self.stdout.write(f'Loaded {len(doctors_data)} doctors')

    def load_treatments(self):
        """Load fake treatments data"""
        treatments_data = [
            {
                'name': 'Dental Cleaning',
                'description': 'Professional teeth cleaning and polishing',
                'price': Decimal('150.00'),
                'duration_minutes': 60,
                'is_active': True
            },
            {
                'name': 'Teeth Whitening',
                'description': 'Professional teeth whitening treatment',
                'price': Decimal('300.00'),
                'duration_minutes': 90,
                'is_active': True
            },
            {
                'name': 'Dental Filling',
                'description': 'Composite or amalgam filling for cavities',
                'price': Decimal('200.00'),
                'duration_minutes': 45,
                'is_active': True
            },
            {
                'name': 'Root Canal',
                'description': 'Endodontic treatment for infected teeth',
                'price': Decimal('800.00'),
                'duration_minutes': 120,
                'is_active': True
            },
            {
                'name': 'Dental Crown',
                'description': 'Porcelain or metal crown placement',
                'price': Decimal('1200.00'),
                'duration_minutes': 90,
                'is_active': True
            },
            {
                'name': 'Tooth Extraction',
                'description': 'Simple or surgical tooth extraction',
                'price': Decimal('250.00'),
                'duration_minutes': 30,
                'is_active': True
            },
            {
                'name': 'Dental Implant',
                'description': 'Titanium implant placement',
                'price': Decimal('2500.00'),
                'duration_minutes': 180,
                'is_active': True
            },
            {
                'name': 'Orthodontic Consultation',
                'description': 'Initial consultation for braces or aligners',
                'price': Decimal('100.00'),
                'duration_minutes': 30,
                'is_active': True
            },
            {
                'name': 'Gum Treatment',
                'description': 'Periodontal treatment for gum disease',
                'price': Decimal('400.00'),
                'duration_minutes': 60,
                'is_active': True
            },
            {
                'name': 'Emergency Visit',
                'description': 'Urgent dental care for pain or trauma',
                'price': Decimal('200.00'),
                'duration_minutes': 30,
                'is_active': True
            }
        ]
        
        for treatment_data in treatments_data:
            Treatment.objects.get_or_create(
                name=treatment_data['name'],
                defaults=treatment_data
            )
        
        self.stdout.write(f'Loaded {len(treatments_data)} treatments')

    def load_patients(self):
        """Load fake patients data"""
        patients_data = [
            {
                'full_name': 'John Smith',
                'phone': '+1-555-1001',
                'email': 'john.smith@email.com',
                'birth_date': datetime(1985, 3, 15).date(),
                'address': '123 Main St, New York, NY 10001',
                'notes': 'Regular patient, prefers morning appointments'
            },
            {
                'full_name': 'Sarah Johnson',
                'phone': '+1-555-1002',
                'email': 'sarah.johnson@email.com',
                'birth_date': datetime(1990, 7, 22).date(),
                'address': '456 Oak Ave, New York, NY 10002',
                'notes': 'Allergic to latex, needs special precautions'
            },
            {
                'full_name': 'Michael Brown',
                'phone': '+1-555-1003',
                'email': 'michael.brown@email.com',
                'birth_date': datetime(1978, 11, 8).date(),
                'address': '789 Pine St, New York, NY 10003',
                'notes': 'High anxiety, needs extra time for procedures'
            },
            {
                'full_name': 'Emily Davis',
                'phone': '+1-555-1004',
                'email': 'emily.davis@email.com',
                'birth_date': datetime(1995, 1, 30).date(),
                'address': '321 Elm St, New York, NY 10004',
                'notes': 'New patient, first visit scheduled'
            },
            {
                'full_name': 'David Wilson',
                'phone': '+1-555-1005',
                'email': 'david.wilson@email.com',
                'birth_date': datetime(1982, 9, 12).date(),
                'address': '654 Maple Ave, New York, NY 10005',
                'notes': 'Prefers Dr. Carter for all treatments'
            },
            {
                'full_name': 'Lisa Anderson',
                'phone': '+1-555-1006',
                'email': 'lisa.anderson@email.com',
                'birth_date': datetime(1988, 5, 18).date(),
                'address': '987 Cedar St, New York, NY 10006',
                'notes': 'Orthodontic treatment in progress'
            },
            {
                'full_name': 'Robert Taylor',
                'phone': '+1-555-1007',
                'email': 'robert.taylor@email.com',
                'birth_date': datetime(1975, 12, 3).date(),
                'address': '147 Birch St, New York, NY 10007',
                'notes': 'Regular cleanings every 6 months'
            },
            {
                'full_name': 'Jennifer Martinez',
                'phone': '+1-555-1008',
                'email': 'jennifer.martinez@email.com',
                'birth_date': datetime(1992, 8, 25).date(),
                'address': '258 Spruce Ave, New York, NY 10008',
                'notes': 'Pregnant, needs special care considerations'
            },
            {
                'full_name': 'Christopher Lee',
                'phone': '+1-555-1009',
                'email': 'christopher.lee@email.com',
                'birth_date': datetime(1980, 4, 14).date(),
                'address': '369 Willow St, New York, NY 10009',
                'notes': 'Diabetic, needs careful monitoring'
            },
            {
                'full_name': 'Amanda Garcia',
                'phone': '+1-555-1010',
                'email': 'amanda.garcia@email.com',
                'birth_date': datetime(1987, 10, 7).date(),
                'address': '741 Ash Ave, New York, NY 10010',
                'notes': 'Insurance: Delta Dental, prefers afternoon appointments'
            }
        ]
        
        for patient_data in patients_data:
            Patient.objects.get_or_create(
                full_name=patient_data['full_name'],
                defaults=patient_data
            )
        
        self.stdout.write(f'Loaded {len(patients_data)} patients')

    def load_leads(self):
        """Load fake leads data"""
        doctors = list(Doctor.objects.filter(is_active=True))
        sources = ['Website', 'Referral', 'Social Media', 'Advertisement', 'Walk-in', 'Phone Call']
        statuses = ['new', 'contacted', 'converted', 'lost']
        
        leads_data = [
            {
                'full_name': 'Alex Thompson',
                'phone': '+1-555-2001',
                'source': 'Website',
                'status': 'new',
                'notes': 'Interested in teeth whitening, found us online'
            },
            {
                'full_name': 'Maria Rodriguez',
                'phone': '+1-555-2002',
                'source': 'Referral',
                'status': 'contacted',
                'notes': 'Referred by John Smith, needs orthodontic consultation'
            },
            {
                'full_name': 'Kevin Park',
                'phone': '+1-555-2003',
                'source': 'Social Media',
                'status': 'converted',
                'notes': 'Saw our Instagram ad, scheduled consultation'
            },
            {
                'full_name': 'Rachel Green',
                'phone': '+1-555-2004',
                'source': 'Advertisement',
                'status': 'contacted',
                'notes': 'Responded to newspaper ad, interested in implants'
            },
            {
                'full_name': 'Tom Wilson',
                'phone': '+1-555-2005',
                'source': 'Walk-in',
                'status': 'new',
                'notes': 'Walked in asking about emergency dental care'
            },
            {
                'full_name': 'Sophie Chen',
                'phone': '+1-555-2006',
                'source': 'Phone Call',
                'status': 'contacted',
                'notes': 'Called asking about pediatric dentistry services'
            },
            {
                'full_name': 'Mark Johnson',
                'phone': '+1-555-2007',
                'source': 'Website',
                'status': 'lost',
                'notes': 'Went to competitor, price was lower'
            },
            {
                'full_name': 'Jessica Brown',
                'phone': '+1-555-2008',
                'source': 'Referral',
                'status': 'converted',
                'notes': 'Referred by Sarah Johnson, scheduled cleaning'
            }
        ]
        
        for i, lead_data in enumerate(leads_data):
            # Assign random doctor to some leads
            assigned_doctor = random.choice(doctors) if random.random() > 0.3 else None
            
            # Create lead with random creation date in the past 30 days
            created_at = timezone.now() - timedelta(days=random.randint(0, 30))
            
            lead = Lead.objects.create(
                full_name=lead_data['full_name'],
                phone=lead_data['phone'],
                source=lead_data['source'],
                assigned_doctor=assigned_doctor,
                status=lead_data['status'],
                notes=lead_data['notes'],
                created_at=created_at
            )
        
        self.stdout.write(f'Loaded {len(leads_data)} leads')

    def load_appointments(self):
        """Load fake appointments data"""
        patients = list(Patient.objects.all())
        doctors = list(Doctor.objects.filter(is_active=True))
        treatments = list(Treatment.objects.filter(is_active=True))
        statuses = ['scheduled', 'completed', 'cancelled']
        
        # Generate appointments for the next 30 days and past 30 days
        appointments = []
        
        for i in range(50):  # Create 50 appointments
            patient = random.choice(patients)
            doctor = random.choice(doctors)
            treatment = random.choice(treatments)
            status = random.choice(statuses)
            
            # Random date within the next 30 days or past 30 days
            days_offset = random.randint(-30, 30)
            appointment_date = (timezone.now() + timedelta(days=days_offset)).date()
            
            # Random time between 9 AM and 5 PM
            hour = random.randint(9, 17)
            minute = random.choice([0, 15, 30, 45])
            appointment_time = datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").time()
            
            # Calculate price based on treatment
            price = treatment.price + Decimal(random.randint(-50, 100))  # Add some variation
            
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                treatment=treatment,
                doctor_name=doctor.name,
                service=treatment.name,
                date=appointment_date,
                time=appointment_time,
                status=status,
                price=price,
                notes=f"Appointment notes for {treatment.name} with {doctor.name}"
            )
            appointments.append(appointment)
        
        self.stdout.write(f'Loaded {len(appointments)} appointments')

    def load_payments(self):
        """Load fake payments data"""
        patients = list(Patient.objects.all())
        payment_types = ['cash', 'card', 'online']
        statuses = ['paid', 'pending']
        
        payments = []
        
        for i in range(30):  # Create 30 payments
            patient = random.choice(patients)
            payment_type = random.choice(payment_types)
            status = random.choice(statuses)
            
            # Random amount between $50 and $2000
            amount = Decimal(random.randint(50, 2000))
            
            # Random date within the past 60 days
            days_offset = random.randint(-60, 0)
            payment_date = timezone.now() + timedelta(days=days_offset)
            
            payment = Payment.objects.create(
                patient=patient,
                amount=amount,
                payment_type=payment_type,
                status=status,
                date=payment_date,
                notes=f"Payment for {payment_type} transaction"
            )
            payments.append(payment)
        
        self.stdout.write(f'Loaded {len(payments)} payments')

    def load_receipts(self):
        """Load fake receipts data"""
        appointments = list(Appointment.objects.filter(status='completed'))
        
        receipts = []
        
        for appointment in appointments[:20]:  # Create receipts for first 20 completed appointments
            receipt = Receipt.objects.create(
                appointment=appointment,
                total_amount=appointment.price,
                services_done=appointment.service,
                created_at=appointment.date
            )
            receipts.append(receipt)
        
        self.stdout.write(f'Loaded {len(receipts)} receipts')
